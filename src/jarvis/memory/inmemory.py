from jarvis.core.config import settings
from jarvis.core.models import Message
from jarvis.memory.base import MemoryBackend


class InMemoryBackend(MemoryBackend):
    """In-memory persistence for Jarvis sessions."""

    def __init__(self) -> None:
        self._sessions: dict[str, list[Message]] = {}

    def get_messages(self, session_id: str) -> list[Message]:
        return self._sessions.get(session_id, [])

    def add_message(self, session_id: str, message: Message) -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = []

        self._sessions[session_id].append(message)

        # Enforce history limit
        if len(self._sessions[session_id]) > settings.memory_max_history:
            self._sessions[session_id] = self._sessions[session_id][-settings.memory_max_history :]

    def clear_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]

    def list_sessions(self) -> list[str]:
        return list(self._sessions.keys())
