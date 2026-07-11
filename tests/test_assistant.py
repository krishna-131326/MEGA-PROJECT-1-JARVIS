import json

import pytest

from jarvis.core.plugin import Plugin
from jarvis.core.router import CommandRouter
from jarvis.llm.base import LLMProvider
from jarvis.memory.inmemory import InMemoryBackend
from jarvis.services.assistant import AssistantService


class MockWeatherPlugin(Plugin):
    @property
    def name(self):
        return "weather"

    @property
    def priority(self):
        return 100

    def can_handle(self, query):
        return False

    async def execute(self, query="", **kwargs):
        return f"Weather is sunny in {kwargs.get('location', 'unknown')}!"

    def get_tool_schema(self):
        return {
            "type": "function",
            "function": {
                "name": "weather",
                "parameters": {"type": "object", "properties": {"location": {"type": "string"}}},
            },
        }


class FakeLLM(LLMProvider):
    def __init__(self, responses):
        self.responses = responses
        self.call_count = 0

    async def generate(self, messages, tools=None):
        resp = self.responses[self.call_count]
        self.call_count += 1
        return resp


@pytest.mark.asyncio
async def test_assistant_tool_loop():
    router = CommandRouter()
    router.register_plugin(MockWeatherPlugin())
    memory = InMemoryBackend()

    llm = FakeLLM(
        [
            # First call returns a tool call
            {
                "tool_calls": [
                    {
                        "function": {
                            "name": "weather",
                            "arguments": json.dumps({"location": "Delhi"}),
                        }
                    }
                ]
            },
            # Second call returns the final response
            "It will be sunny in Delhi!",
        ]
    )

    assistant = AssistantService(router, llm, memory)
    response = await assistant.process("What is the weather in Delhi?", session_id="test")

    assert response.source == "llm"
    assert response.response == "It will be sunny in Delhi!"
    assert llm.call_count == 2

    messages = memory.get_messages("test")
    assert any(
        m.role == "tool" and m.tool == "weather" and "sunny in Delhi" in m.content for m in messages
    )


@pytest.mark.asyncio
async def test_assistant_loop_limit():
    router = CommandRouter()
    memory = InMemoryBackend()

    # Always return a tool call to simulate an infinite loop
    llm = FakeLLM([{"tool_calls": [{"function": {"name": "unknown_tool", "arguments": "{}"}}]}] * 6)

    assistant = AssistantService(router, llm, memory)
    response = await assistant.process("infinite loop test", session_id="test2")

    assert "internal loop limit" in response.response
    assert llm.call_count == 5  # MAX_TOOL_CALLS is 5
