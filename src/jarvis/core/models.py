from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Any


class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tool: Optional[str] = None
    tool_calls: Optional[list[dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


class AssistantResponse(BaseModel):
    response: str
    source: str  # "plugin" or "llm"
    plugin_used: Optional[str] = None
