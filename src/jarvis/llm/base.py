from abc import ABC, abstractmethod
from typing import List, Optional

class LLMProvider(ABC):
    """Base interface for Language Model providers."""
    
    @abstractmethod
    def generate(self, prompt: str, context: Optional[List[str]] = None) -> str:
        """Generates a response from the LLM based on the prompt and context."""
        pass
