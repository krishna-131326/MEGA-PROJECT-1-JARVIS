from abc import ABC, abstractmethod


class Plugin(ABC):
    """Base class for all Jarvis plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the plugin."""
        pass

    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """Returns True if the plugin can handle the given query."""
        pass

    @abstractmethod
    def execute(self, query: str) -> str:
        """Executes the query and returns a response string."""
        pass
