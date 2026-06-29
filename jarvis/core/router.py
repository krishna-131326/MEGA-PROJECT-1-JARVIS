"""Deterministic routing for commands that do not require an LLM."""

from types import MappingProxyType
from urllib.parse import urlparse

from jarvis.core.models import Action, Command

_SITE_URLS = MappingProxyType(
    {
        "google": "https://google.com",
        "facebook": "https://facebook.com",
        "youtube": "https://youtube.com",
        "linkedin": "https://linkedin.com",
    }
)


def parse_command(text: str) -> Command:
    """Parse user text without performing browser, audio, file, or network I/O."""

    raw_text = text
    normalized = " ".join(text.casefold().split())
    if not normalized:
        return Command(action=Action.UNKNOWN, raw_text=raw_text)

    if normalized == "news" or normalized.startswith("news "):
        return Command(action=Action.GET_NEWS, raw_text=raw_text)

    verb, separator, value = normalized.partition(" ")
    if not separator or not value:
        return Command(action=Action.UNKNOWN, raw_text=raw_text)

    if verb == "open" and value in _SITE_URLS:
        url = _SITE_URLS[value]
        _validate_http_url(url)
        return Command(
            action=Action.OPEN_URL,
            arguments=MappingProxyType({"url": url}),
            raw_text=raw_text,
        )

    if verb == "search":
        return Command(
            action=Action.SEARCH_WEB,
            arguments=MappingProxyType({"query": value}),
            raw_text=raw_text,
        )

    if verb == "play":
        return Command(
            action=Action.PLAY_MUSIC,
            arguments=MappingProxyType({"song": value}),
            raw_text=raw_text,
        )

    return Command(action=Action.UNKNOWN, raw_text=raw_text)


def _validate_http_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Unsupported browser URL: {url!r}")

