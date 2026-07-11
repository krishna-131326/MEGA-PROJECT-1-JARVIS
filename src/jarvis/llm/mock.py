from typing import Any

from jarvis.core.models import Message
from jarvis.llm.base import LLMProvider


class MockProvider(LLMProvider):
    """A mock LLM provider for testing and fallback."""

    async def generate(
        self, messages: list[Message], tools: list[dict[str, Any]] | None = None
    ) -> str | dict[str, Any]:
        prompt = messages[-1].content if messages else "empty"
        return f"Mock response to: {prompt}"
