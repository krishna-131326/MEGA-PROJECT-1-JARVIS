from abc import ABC, abstractmethod


class Plugin(ABC):
    """Base class for all Jarvis plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the plugin (for tool calling and internal routing)."""
        pass
        
    @property
    def priority(self) -> int:
        """Priority for deterministic routing (lower means evaluated first). Default is 100."""
        return 100

    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """Returns True if the plugin can handle the given query."""
        pass

    @abstractmethod
    async def execute(self, query: str = "", **kwargs) -> str:
        """Executes the command. Supports direct query or structured **kwargs from tool calls."""
        pass
        
    def get_tool_schema(self) -> dict | None:
        """Returns the OpenAI-compatible function definition for LLM tool calling. Override if the plugin supports it."""
        return None
