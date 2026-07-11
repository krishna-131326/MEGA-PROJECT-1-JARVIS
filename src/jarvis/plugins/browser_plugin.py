import webbrowser
from typing import Any

from jarvis.core.plugin import Plugin


class BrowserPlugin(Plugin):
    @property
    def name(self) -> str:
        return "browser"

    @property
    def priority(self) -> int:
        return 100

    def can_handle(self, query: str) -> bool:
        return "open" in query.lower() or "search" in query.lower()

    def get_tool_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Open a website or search the web in the user's browser. WARNING: This only opens the user's local browser window, it DOES NOT return search results or website text back to you.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform, e.g., 'open google', 'search kittens'.",
                        }
                    },
                    "required": ["action"],
                },
            },
        }

    async def execute(self, query: str = "", **kwargs: Any) -> str:
        q = kwargs.get("action", query).lower()
        if "open google" in q:
            webbrowser.open("https://google.com")
            return "Opening Google."
        elif "open facebook" in q:
            webbrowser.open("https://facebook.com")
            return "Opening Facebook."
        elif "open youtube" in q:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube."
        elif "open linkedin" in q:
            webbrowser.open("https://linkedin.com")
            return "Opening LinkedIn."
        elif q.startswith("search"):
            parts = q.split(" ", 1)
            if len(parts) > 1:
                search_query = parts[1].replace(" ", "+")
                webbrowser.open(f"https://www.bing.com/search?q={search_query}")
                return f"Searching for {parts[1]}."
            return "What do you want me to search for?"

        return "I can't open that website yet."
