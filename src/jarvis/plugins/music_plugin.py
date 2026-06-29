from jarvis.core.plugin import Plugin
from jarvis.providers.music_provider import MusicProvider


class MusicPlugin(Plugin):
    def __init__(self, provider: MusicProvider):
        self.provider = provider

    @property
    def name(self) -> str:
        return "MusicPlugin"

    def can_handle(self, query: str) -> bool:
        return query.lower().startswith("play")

    def execute(self, query: str) -> str:
        parts = query.lower().split(" ", 1)
        if len(parts) > 1:
            song_name = parts[1]
            return self.provider.play(song_name)
        return "Please tell me what song to play."
