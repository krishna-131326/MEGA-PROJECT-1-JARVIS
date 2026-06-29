from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Base interface for Language Model providers."""

    @abstractmethod
    def generate(self, prompt: str, context: list[str] | None = None) -> str:
        """Generates a response from the LLM based on the prompt and context."""
        pass
