from typing import List, Optional
from jarvis.llm.base import LLMProvider

class MockProvider(LLMProvider):
    """A mock LLM provider for testing and fallback."""
    
    def generate(self, prompt: str, context: Optional[List[str]] = None) -> str:
        return f"Mock response to: {prompt}"
