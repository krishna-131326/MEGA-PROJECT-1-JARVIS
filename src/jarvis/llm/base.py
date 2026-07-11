from abc import ABC, abstractmethod
from typing import Any

from jarvis.core.models import Message


class LLMProvider(ABC):
    """Base interface for Language Model providers."""

    @abstractmethod
    async def generate(
        self, messages: list[Message], tools: list[dict[str, Any]] | None = None
    ) -> str | dict[str, Any]:
        """Generates a response from the LLM based on the message history and available tools.
        Returns either a string (response text) or a dict (representing a tool call).
        """
        pass
