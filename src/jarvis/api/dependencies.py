from typing import Generator
from jarvis.llm.base import LLMProvider
from jarvis.core.router import CommandRouter
from jarvis.core.config import settings
from jarvis.llm.grok import GrokProvider
from jarvis.llm.mock import MockProvider
from jarvis.plugins.browser_plugin import BrowserPlugin
from jarvis.plugins.music_plugin import MusicPlugin
from jarvis.plugins.news_plugin import NewsPlugin
from jarvis.providers.music_provider import WebMusicProvider
from jarvis.services.assistant import AssistantService


def get_router() -> CommandRouter:
    router = CommandRouter()
    music_provider = WebMusicProvider(config_path=settings.music_config_path)
    router.register_plugin(NewsPlugin())
    router.register_plugin(BrowserPlugin())
    router.register_plugin(MusicPlugin(provider=music_provider))
    return router


def get_llm() -> LLMProvider:
    if settings.grok_api_key:
        return GrokProvider(api_key=settings.grok_api_key)
    return MockProvider()


from jarvis.memory.inmemory import InMemoryBackend

# We can cache the service so we don't recreate it on every request
_memory_backend = InMemoryBackend()
_assistant_service = AssistantService(get_router(), get_llm(), _memory_backend)


def get_assistant() -> AssistantService:
    return _assistant_service
