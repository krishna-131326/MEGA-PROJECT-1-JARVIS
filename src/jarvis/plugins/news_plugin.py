import logging

import httpx

from typing import Any
from jarvis.core.config import settings
from jarvis.core.plugin import Plugin

logger = logging.getLogger(__name__)


class NewsPlugin(Plugin):
    @property
    def name(self) -> str:
        return "news"
        
    @property
    def priority(self) -> int:
        return 100

    def can_handle(self, query: str) -> bool:
        # Only use fast-path for exact simple commands
        return query.strip().lower() in ["news", "top news", "latest news"]

    async def execute(self, query: str = "", limit: int = 5, topic: str = "", **kwargs: str) -> str:
        api_key = settings.news_api_key
        if not api_key:
            return "News is unavailable because NEWS_API_KEY is not configured."

        try:
            # If kwargs has 'limit' or 'topic', use them (called via tool)
            limit = int(kwargs.get("limit", limit))
            topic = kwargs.get("topic", topic)
            
            # If fast path, we might extract topic from query if we wanted to, but we'll keep it simple
            
            params = {"country": "us"}
            if topic:
                params["q"] = topic
            
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://newsapi.org/v2/top-headlines",
                    headers={"X-Api-Key": api_key},
                    params=params,
                    timeout=10,
                )
                r.raise_for_status()
                data = r.json()
            articles = data.get("articles", [])

            if not articles:
                return f"I couldn't find any news at the moment{' for ' + topic if topic else ''}."

            # If called as a tool (by LLM), returning raw data or clean text is fine. 
            # We return a formatted string that the LLM can easily read.
            headlines = []
            for article in articles[:limit]:
                title = article.get("title", "")
                if title:
                    headlines.append(title)
            
            if not headlines:
                return "No valid headlines found."
                
            return f"Top headlines{' for ' + topic if topic else ''}:\n" + "\n".join(f"- {h}" for h in headlines)

        except Exception as e:
            logger.error(f"Failed to fetch news: {e}")
            return "There was an error retrieving the news."

    def get_tool_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Fetch the latest top news headlines, optionally filtered by a specific topic and limited to a certain number.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The specific topic to search for (e.g., 'Apple', 'Technology', 'Sports'). Leave empty for general top headlines."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "The number of headlines to fetch (default is 5, max 20)."
                        }
                    },
                    "required": []
                }
            }
        }
