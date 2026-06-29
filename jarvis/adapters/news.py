"""NewsAPI adapter with bounded network behavior."""

from dataclasses import dataclass

import requests


class NewsConfigurationError(RuntimeError):
    """Raised when the NewsAPI adapter has no credential."""


class NewsServiceError(RuntimeError):
    """Raised when NewsAPI cannot return a valid response."""


@dataclass(frozen=True, slots=True)
class NewsApiReader:
    """Fetch headlines from NewsAPI without placing credentials in URLs."""

    api_key: str
    timeout_seconds: float = 10.0
    endpoint: str = "https://newsapi.org/v2/top-headlines"

    def __post_init__(self) -> None:
        if not self.api_key.strip():
            raise NewsConfigurationError("NEWS_API_KEY is not configured.")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive.")

    def headlines(self, *, country: str) -> tuple[str, ...]:
        try:
            response = requests.get(
                self.endpoint,
                headers={"X-Api-Key": self.api_key},
                params={"country": country},
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            document = response.json()
        except (requests.RequestException, ValueError) as error:
            raise NewsServiceError("Unable to retrieve headlines.") from error

        articles = document.get("articles")
        if not isinstance(articles, list):
            raise NewsServiceError("NewsAPI returned an invalid articles field.")

        return tuple(
            title.strip()
            for article in articles
            if isinstance(article, dict)
            and isinstance((title := article.get("title")), str)
            and title.strip()
        )

