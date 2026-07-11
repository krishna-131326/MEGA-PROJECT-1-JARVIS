from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    mode: str = "chat"
    stream: bool = False


class ChatResponse(BaseModel):
    response: str
    source: str
    plugin_used: Optional[str] = None
    timestamp: datetime = datetime.now(timezone.utc)


class HealthResponse(BaseModel):
    status: str
    version: str
    llm: str
    plugins: int
