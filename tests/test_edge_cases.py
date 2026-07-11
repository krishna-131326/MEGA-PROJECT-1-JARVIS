import pytest
from unittest.mock import patch, mock_open
import httpx
from jarvis.plugins.news_plugin import NewsPlugin
from jarvis.plugins.browser_plugin import BrowserPlugin
from jarvis.plugins.music_plugin import MusicPlugin
from jarvis.providers.music_provider import WebMusicProvider
from jarvis.core.router import CommandRouter
from jarvis.core.plugin import Plugin
from jarvis.core.config import settings


class FaultyPlugin(Plugin):
    @property
    def name(self) -> str:
        return "FaultyPlugin"

    def can_handle(self, query: str) -> bool:
        return "crash" in query.lower()

    async def execute(self, query: str) -> str:
        raise ValueError("Simulated crash")


@pytest.mark.asyncio
@patch("jarvis.plugins.news_plugin.settings")
async def test_news_plugin_missing_key(mock_settings):
    mock_settings.news_api_key = ""
    plugin = NewsPlugin()
    response = await plugin.execute("news")
    assert response == "News is unavailable because NEWS_API_KEY is not configured."


@pytest.mark.asyncio
async def test_browser_plugin_unknown_site():
    plugin = BrowserPlugin()
    response = await plugin.execute("open somerandomsite")
    assert response == "I can't open that website yet."


@pytest.mark.asyncio
async def test_browser_plugin_empty_search():
    plugin = BrowserPlugin()
    response = await plugin.execute("search")
    assert response == "What do you want me to search for?"


@pytest.mark.asyncio
@patch("jarvis.plugins.browser_plugin.webbrowser.open")
async def test_browser_plugin_search_success(mock_open):
    plugin = BrowserPlugin()
    response = await plugin.execute("search python programming")
    assert response == "Searching for python programming."
    mock_open.assert_called_once_with("https://www.bing.com/search?q=python+programming")


@pytest.mark.asyncio
async def test_music_plugin_empty_query():
    provider = WebMusicProvider("dummy.json")
    plugin = MusicPlugin(provider)
    response = await plugin.execute("play")
    assert response == "Please tell me what song to play."
