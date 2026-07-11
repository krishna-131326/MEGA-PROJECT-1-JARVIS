from datetime import UTC, datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    mode: str = "chat"
    stream: bool = False


class ChatResponse(BaseModel):
    response: str
    source: str
    plugin_used: str | None = None
    timestamp: datetime = datetime.now(UTC)


class HealthResponse(BaseModel):
    status: str
    version: str
    llm: str
    plugins: int
