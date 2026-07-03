from jarvis.core.plugin import Plugin
from jarvis.providers.music_provider import MusicProvider


class MusicPlugin(Plugin):
    def __init__(self, provider: MusicProvider):
        self.provider = provider

    @property
    def name(self) -> str:
        return "music"
        
    @property
    def priority(self) -> int:
        return 50

    def can_handle(self, query: str) -> bool:
        return query.lower().startswith("play")

        return "Please tell me what song to play."
        
    def get_tool_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Play a specific song.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "song_name": {
                            "type": "string",
                            "description": "The name of the song to play."
                        }
                    },
                    "required": ["song_name"]
                }
            }
        }

    async def execute(self, query: str = "", **kwargs) -> str:
        song_name = kwargs.get("song_name")
        if not song_name:
            parts = query.lower().split(" ", 1)
            if len(parts) > 1:
                song_name = parts[1]
        
        if song_name:
            return self.provider.play(song_name)
        return "Please tell me what song to play."
