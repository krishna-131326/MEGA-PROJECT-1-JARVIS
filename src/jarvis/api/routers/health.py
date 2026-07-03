from fastapi import APIRouter, Depends
from jarvis.api.schemas import HealthResponse
from jarvis.api.dependencies import get_assistant
from jarvis.services.assistant import AssistantService

router = APIRouter(tags=["health"])

@router.get("/health", response_model=HealthResponse)
async def health_check(assistant: AssistantService = Depends(get_assistant)):
    llm_status = "connected" if assistant.llm.__class__.__name__ != "MockProvider" else "mocked"
    return HealthResponse(
        status="healthy",
        version="0.2.0",
        llm=llm_status,
        plugins=len(assistant.router.plugins)
    )

@router.get("/ready")
async def readiness_check(assistant: AssistantService = Depends(get_assistant)):
    # Simulates checking DB, external services, etc.
    return {"status": "ready"}

@router.get("/api/plugins")
async def get_plugins(assistant: AssistantService = Depends(get_assistant)):
    plugins = []
    for plugin in assistant.router.plugins:
        plugins.append({
            "name": plugin.name,
            "enabled": True
        })
    return plugins

