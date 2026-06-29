import logging

import requests

from jarvis.core.config import settings
from jarvis.core.plugin import Plugin

logger = logging.getLogger(__name__)


class NewsPlugin(Plugin):
    @property
    def name(self) -> str:
        return "NewsPlugin"

    def can_handle(self, query: str) -> bool:
        return "news" in query.lower()

    def execute(self, query: str) -> str:
        api_key = settings.news_api_key
        if not api_key:
            return "News is unavailable because NEWS_API_KEY is not configured."

        try:
            r = requests.get(
                "https://newsapi.org/v2/top-headlines",
                headers={"X-Api-Key": api_key},
                params={"country": "us"},
                timeout=10,
            )
            r.raise_for_status()
            data = r.json()
            articles = data.get("articles", [])

            if not articles:
                return "I couldn't find any news at the moment."

            headlines = [article["title"] for article in articles[:5] if article.get("title")]
            return "Here are the top headlines:\n" + "\n".join(f"- {h}" for h in headlines)

        except Exception as e:
            logger.error(f"Failed to fetch news: {e}")
            return "There was an error retrieving the news."
