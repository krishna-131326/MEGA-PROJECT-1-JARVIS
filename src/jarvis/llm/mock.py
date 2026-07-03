from jarvis.llm.base import LLMProvider


class MockProvider(LLMProvider):
    """A mock LLM provider for testing and fallback."""

    async def generate(self, prompt: str, context: list[str] | None = None) -> str:
        return f"Mock response to: {prompt}"
