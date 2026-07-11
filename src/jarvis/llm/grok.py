import logging
from typing import Any, cast

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from jarvis.core.config import settings
from jarvis.core.models import Message
from jarvis.llm.base import LLMProvider

logger = logging.getLogger(__name__)


class GrokProvider(LLMProvider):
    """Grok (xAI) LLM Provider implementation using httpx and tenacity for retries."""

    def __init__(self, api_key: str, model: str | None = None):
        self.api_key = api_key.strip("`'\" ")  # In case they have backticks
        self.is_groq = self.api_key.startswith("gsk_")

        # Default model logic based on provider
        if model:
            self.model = model
        else:
            if self.is_groq and settings.grok_model == "grok-beta":
                self.model = "llama-3.1-8b-instant"
            else:
                self.model = settings.grok_model

        if not self.api_key:
            logger.warning("Grok API key is missing. GrokProvider will not function correctly.")

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def _call_api(
        self, messages: list[Message], tools: list[dict[str, Any]] | None = None
    ) -> str | dict[str, Any]:
        system_content = (
            "You are Jarvis, a helpful AI assistant. "
            "You must use the provided tools to fulfill requests. "
            "CRITICAL: The user's chat interface DOES NOT display tool outputs. The user CANNOT see the data returned by tools. "
            "Because the user is blind to tool results, you MUST explicitly write out the information you find into your conversational response. "
            "Do NOT say 'I have fetched the news' or 'Here is the data' without actually printing the data. You must literally include the fetched information in your message. "
            "Exception: If a tool specifically states it 'opened a browser' or 'played music' locally, just inform the user you performed the action. "
            "DO NOT output raw JSON in your text response."
        )
        api_messages: list[dict[str, Any]] = [{"role": "system", "content": system_content}]

        for msg in messages:
            if msg.role == "assistant" and msg.tool_calls:
                api_messages.append(
                    {
                        "role": "assistant",
                        "content": msg.content or "",
                        "tool_calls": msg.tool_calls,
                    }
                )
            elif msg.role == "tool":
                api_messages.append(
                    {
                        "role": "tool",
                        "name": msg.tool,
                        "content": msg.content,
                        "tool_call_id": msg.tool_call_id or f"call_{msg.tool}",
                    }
                )
            else:
                api_messages.append({"role": msg.role, "content": msg.content})

        payload = {
            "messages": api_messages,
            "model": self.model,
            "stream": False,
            "temperature": 0.7,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        api_base = (
            "https://api.groq.com/openai/v1/chat/completions"
            if self.is_groq
            else "https://api.x.ai/v1/chat/completions"
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_base,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=15.0,
            )
            response.raise_for_status()
            data = response.json()
            message_obj = data["choices"][0]["message"]

            if message_obj.get("tool_calls"):
                return cast(dict[str, Any], message_obj)  # Return the whole dict for tool handling

            return str(message_obj.get("content", ""))

    async def generate(
        self, messages: list[Message], tools: list[dict[str, Any]] | None = None
    ) -> str | dict[str, Any]:
        logger.info(f"Grok generating response for {len(messages)} messages.")
        if not self.api_key:
            return "Error: Grok API key is not configured."

        try:
            return await self._call_api(messages, tools)
        except Exception as e:
            logger.error(f"Grok API call failed after retries: {e}")
            raise Exception("I'm currently unable to reach my language model provider.") from e
