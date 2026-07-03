import pytest
from jarvis.plugins.news_plugin import NewsPlugin
from jarvis.plugins.browser_plugin import BrowserPlugin
from jarvis.plugins.music_plugin import MusicPlugin
from jarvis.providers.music_provider import WebMusicProvider

def test_news_plugin_can_handle():
    plugin = NewsPlugin()
    assert plugin.can_handle("what's the news") is True
    assert plugin.can_handle("tell me a joke") is False

def test_browser_plugin_can_handle():
    plugin = BrowserPlugin()
    assert plugin.can_handle("open google") is True
    assert plugin.can_handle("search python") is True
    assert plugin.can_handle("play music") is False

def test_music_plugin_can_handle():
    provider = WebMusicProvider("dummy.json")
    plugin = MusicPlugin(provider)
    assert plugin.can_handle("play believer") is True
    assert plugin.can_handle("stop") is False

@pytest.mark.asyncio
async def test_music_plugin_execute():
    class DummyProvider:
        def play(self, song):
            return f"Playing {song}"
    
    plugin = MusicPlugin(DummyProvider())
    response = await plugin.execute("play believer")
    assert response == "Playing believer"

def test_plugin_metadata():
    plugin = NewsPlugin()
    assert plugin.name == "news"
    assert plugin.priority == 100
    
    schema = plugin.get_tool_schema()
    assert schema is not None
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "news"

