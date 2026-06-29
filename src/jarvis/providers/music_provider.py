from abc import ABC, abstractmethod
import json
import logging
from pathlib import Path
import webbrowser

logger = logging.getLogger(__name__)

class MusicProvider(ABC):
    """Base class for music providers."""
    
    @abstractmethod
    def play(self, song_name: str) -> str:
        pass

class WebMusicProvider(MusicProvider):
    """Provides music by opening web links (e.g., YouTube) configured in a JSON file."""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.songs = self._load_config()

    def _load_config(self) -> dict:
        path = Path(self.config_path)
        if not path.exists():
            logger.warning(f"Music config not found at {self.config_path}")
            return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("songs", {})
        except Exception as e:
            logger.error(f"Failed to load music config: {e}")
            return {}

    def play(self, song_name: str) -> str:
        song_url = self.songs.get(song_name.lower())
        if song_url:
            webbrowser.open(song_url)
            return f"Playing {song_name} on the web."
        return f"Could not find song: {song_name}"

class LocalMusicProvider(MusicProvider):
    """Provides music by playing local files (placeholder for future implementation)."""
    
    def play(self, song_name: str) -> str:
        # Future implementation for playing local MP3s
        return f"Local playback for {song_name} is not yet implemented."
