import logging
import json
from jarvis.core.router import CommandRouter
from jarvis.llm.base import LLMProvider
from jarvis.memory.base import MemoryBackend
from jarvis.core.models import Message, AssistantResponse

logger = logging.getLogger(__name__)


class AssistantService:
    def __init__(self, router: CommandRouter, llm: LLMProvider, memory: MemoryBackend):
        self.router = router
        self.llm = llm
        self.memory = memory

    async def process(self, query: str, session_id: str = "default") -> AssistantResponse:
        """
        Processes a user query with dual-path routing (deterministic vs agentic).
        """
        # Save user message to memory
        self.memory.add_message(session_id, Message(role="user", content=query))

        # 1. Fast Path: Deterministic Routing
        plugin = self.router.match(query)
        if plugin:
            try:
                logger.info(f"Fast path executing query via {plugin.name}")
                response_text = await plugin.execute(query)
                self.memory.add_message(
                    session_id, Message(role="assistant", content=response_text)
                )
                return AssistantResponse(
                    response=response_text, source="plugin", plugin_used=plugin.name
                )
            except Exception as e:
                logger.error(f"Plugin {plugin.name} failed on fast path: {e}")
                err_msg = f"Error executing command via {plugin.name}."
                self.memory.add_message(session_id, Message(role="assistant", content=err_msg))
                return AssistantResponse(response=err_msg, source="plugin", plugin_used=plugin.name)

        # 2. LLM Path: Agent Loop
        logger.info("No deterministic match. Falling back to LLM path.")

        # Collect tools
        tools = []
        plugins_map = {}
        for p in self.router.plugins:
            schema = p.get_tool_schema()
            if schema:
                tools.append(schema)
                plugins_map[schema["function"]["name"]] = p

        MAX_TOOL_CALLS = 5
        visited_tools = set()

        for i in range(MAX_TOOL_CALLS):
            messages = self.memory.get_messages(session_id)

            try:
                response = await self.llm.generate(messages, tools=tools if tools else None)
            except Exception as e:
                logger.error(f"LLM generation failed: {e}")
                err_msg = "I'm currently unable to reach my language model provider."
                self.memory.add_message(session_id, Message(role="assistant", content=err_msg))
                return AssistantResponse(response=err_msg, source="llm")

            # Handle direct text response
            if isinstance(response, str):
                self.memory.add_message(session_id, Message(role="assistant", content=response))
                return AssistantResponse(response=response, source="llm")

            # Handle tool calls
            tool_calls = response.get("tool_calls", [])
            if not tool_calls:
                content = response.get("content", "")
                self.memory.add_message(session_id, Message(role="assistant", content=content))
                return AssistantResponse(response=content, source="llm")

            # We have tool calls
            # Save the assistant's request to use tools into memory
            self.memory.add_message(
                session_id, Message(role="assistant", content="", tool_calls=tool_calls)
            )

            for tc in tool_calls:
                func_name = tc["function"]["name"]
                args = tc["function"]["arguments"]
                tc_id = tc.get("id", f"call_{func_name}")

                logger.info(f"LLM requested tool call: {func_name}")
                visited_tools.add(func_name)

                try:
                    kwargs = json.loads(args)
                except:
                    kwargs = {}

                if func_name in plugins_map:
                    try:
                        tool_result = await plugins_map[func_name].execute(**kwargs)
                    except Exception as e:
                        tool_result = f"Tool error: {str(e)}"
                else:
                    tool_result = f"Tool {func_name} not found."

                # Add tool result to memory with proper tool_call_id
                self.memory.add_message(
                    session_id,
                    Message(role="tool", content=tool_result, tool=func_name, tool_call_id=tc_id),
                )

        # Loop limit reached
        err_msg = "I've hit my internal loop limit trying to solve this task."
        self.memory.add_message(session_id, Message(role="assistant", content=err_msg))
        return AssistantResponse(response=err_msg, source="llm")
