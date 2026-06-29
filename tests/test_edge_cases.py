import pytest
from unittest.mock import patch, mock_open
import requests
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
    def execute(self, query: str) -> str:
        raise ValueError("Simulated crash")

def test_router_handles_plugin_exception():
    router = CommandRouter()
    router.register_plugin(FaultyPlugin())
    response = router.route("please crash")
    assert response == "Error executing command via FaultyPlugin."

@patch('jarvis.plugins.news_plugin.settings')
def test_news_plugin_missing_key(mock_settings):
    mock_settings.news_api_key = ""
    plugin = NewsPlugin()
    response = plugin.execute("news")
    assert response == "News is unavailable because NEWS_API_KEY is not configured."

@patch('jarvis.plugins.news_plugin.requests.get')
@patch('jarvis.plugins.news_plugin.settings')
def test_news_plugin_api_error(mock_settings, mock_get):
    mock_settings.news_api_key = "fake_key"
    mock_get.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
    plugin = NewsPlugin()
    response = plugin.execute("news")
    assert response == "There was an error retrieving the news."

@patch('jarvis.plugins.news_plugin.requests.get')
@patch('jarvis.plugins.news_plugin.settings')
def test_news_plugin_empty_articles(mock_settings, mock_get):
    mock_settings.news_api_key = "fake_key"
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"articles": []}
    plugin = NewsPlugin()
    response = plugin.execute("news")
    assert response == "I couldn't find any news at the moment."

def test_browser_plugin_unknown_site():
    plugin = BrowserPlugin()
    response = plugin.execute("open somerandomsite")
    assert response == "I can't open that website yet."

def test_browser_plugin_empty_search():
    plugin = BrowserPlugin()
    response = plugin.execute("search")
    assert response == "What do you want me to search for?"

@patch('jarvis.plugins.browser_plugin.webbrowser.open')
def test_browser_plugin_search_success(mock_open):
    plugin = BrowserPlugin()
    response = plugin.execute("search python programming")
    assert response == "Searching for python programming."
    mock_open.assert_called_once_with("https://www.bing.com/search?q=python+programming")

def test_music_plugin_empty_query():
    provider = WebMusicProvider("dummy.json")
    plugin = MusicPlugin(provider)
    response = plugin.execute("play")
    assert response == "Please tell me what song to play."

@patch('builtins.open', mock_open(read_data='{"songs": {"believer": "http://youtube.com/believer"}}'))
@patch('pathlib.Path.exists', return_value=True)
def test_web_music_provider_success(mock_exists):
    provider = WebMusicProvider("dummy.json")
    assert provider.songs == {"believer": "http://youtube.com/believer"}
    
    with patch('jarvis.providers.music_provider.webbrowser.open') as mock_browser:
        response = provider.play("believer")
        assert response == "Playing believer on the web."
        mock_browser.assert_called_once_with("http://youtube.com/believer")

@patch('pathlib.Path.exists', return_value=False)
def test_web_music_provider_missing_config(mock_exists):
    provider = WebMusicProvider("dummy.json")
    assert provider.songs == {}
    response = provider.play("believer")
    assert response == "Could not find song: believer"

@patch('builtins.open', mock_open(read_data='invalid json'))
@patch('pathlib.Path.exists', return_value=True)
def test_web_music_provider_invalid_json(mock_exists):
    provider = WebMusicProvider("dummy.json")
    assert provider.songs == {}
