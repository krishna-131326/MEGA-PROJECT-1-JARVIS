from abc import ABC, abstractmethod
from typing import List
from jarvis.core.models import Message


class MemoryBackend(ABC):
    """Abstract base class for memory persistence."""

    @abstractmethod
    def get_messages(self, session_id: str) -> List[Message]:
        """Retrieve the conversation history for a given session."""
        pass

    @abstractmethod
    def add_message(self, session_id: str, message: Message) -> None:
        """Add a message to a session's conversation history."""
        pass

    @abstractmethod
    def clear_session(self, session_id: str) -> None:
        """Clear all messages for a given session."""
        pass

    @abstractmethod
    def list_sessions(self) -> List[str]:
        """List all active session IDs."""
        pass
