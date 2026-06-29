import webbrowser
from jarvis.core.plugin import Plugin

class BrowserPlugin(Plugin):
    @property
    def name(self) -> str:
        return "BrowserPlugin"

    def can_handle(self, query: str) -> bool:
        return "open" in query.lower() or "search" in query.lower()

    def execute(self, query: str) -> str:
        q = query.lower()
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
