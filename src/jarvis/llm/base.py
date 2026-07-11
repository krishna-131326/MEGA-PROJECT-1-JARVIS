from abc import ABC, abstractmethod
from typing import List, Optional, Any

from jarvis.core.models import Message


class LLMProvider(ABC):
    """Base interface for Language Model providers."""

    @abstractmethod
    async def generate(
        self, messages: List[Message], tools: Optional[List[dict[str, Any]]] = None
    ) -> str | dict[str, Any]:
        """Generates a response from the LLM based on the message history and available tools.
        Returns either a string (response text) or a dict (representing a tool call).
        """
        pass
