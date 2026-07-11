from typing import List, Optional, Any
from jarvis.llm.base import LLMProvider
from jarvis.core.models import Message


class MockProvider(LLMProvider):
    """A mock LLM provider for testing and fallback."""

    async def generate(
        self, messages: List[Message], tools: Optional[List[dict[str, Any]]] = None
    ) -> str | dict[str, Any]:
        prompt = messages[-1].content if messages else "empty"
        return f"Mock response to: {prompt}"
