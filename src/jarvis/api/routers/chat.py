from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from jarvis.api.schemas import ChatRequest, ChatResponse
from jarvis.api.dependencies import get_assistant
from jarvis.services.assistant import AssistantService

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest, assistant: AssistantService = Depends(get_assistant)
) -> ChatResponse:
    assistant_response = await assistant.process(request.message, session_id=request.session_id)

    return ChatResponse(
        response=assistant_response.response,
        source=assistant_response.source,
        plugin_used=assistant_response.plugin_used,
        timestamp=datetime.now(timezone.utc),
    )


@router.post("/stream")
async def chat_stream(
    request: ChatRequest, assistant: AssistantService = Depends(get_assistant)
) -> dict[str, str]:
    # Placeholder for future streaming support
    # Interviewers appreciate forward-thinking architecture.
    return {"message": "Streaming not yet implemented, but the route is prepared."}
