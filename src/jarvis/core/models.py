from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    tool: str | None = None
    tool_calls: list[dict[str, Any]] | None = None
    tool_call_id: str | None = None


class AssistantResponse(BaseModel):
    response: str
    source: str  # "plugin" or "llm"
    plugin_used: str | None = None
