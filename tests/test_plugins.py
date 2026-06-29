import pytest
from jarvis.plugins.news_plugin import NewsPlugin
from jarvis.plugins.browser_plugin import BrowserPlugin
from jarvis.plugins.music_plugin import MusicPlugin
from jarvis.providers.music_provider import MusicProvider

class MockMusicProvider(MusicProvider):
    def play(self, song_name: str) -> str:
        return f"Mock playing {song_name}"

def test_news_plugin_can_handle():
    plugin = NewsPlugin()
    assert plugin.can_handle("what is the news") is True
    assert plugin.can_handle("tell me a joke") is False

def test_browser_plugin_can_handle():
    plugin = BrowserPlugin()
    assert plugin.can_handle("open google") is True
    assert plugin.can_handle("search for Python") is True
    assert plugin.can_handle("play music") is False

def test_music_plugin_can_handle():
    plugin = MusicPlugin(provider=MockMusicProvider())
    assert plugin.can_handle("play believer") is True
    assert plugin.can_handle("open youtube") is False

def test_music_plugin_execute():
    plugin = MusicPlugin(provider=MockMusicProvider())
    response = plugin.execute("play believer")
    assert response == "Mock playing believer"
