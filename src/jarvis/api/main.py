import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from jarvis.api.routers import chat, health

app = FastAPI(
    title="Jarvis AI Assistant",
    version="0.2.0",
    description="Production-grade AI assistant backend.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(health.router)

# Serve static files (Web UI)
web_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
app.mount("/app", StaticFiles(directory=web_dir, html=True), name="web")


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Redirect to the Web UI."""
    return RedirectResponse(url="/app")
