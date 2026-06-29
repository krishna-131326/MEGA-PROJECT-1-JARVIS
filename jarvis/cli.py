"""Text-only entry point that can run without microphone or audio hardware."""

import os
import sys

import musicLibrary

from jarvis.adapters.browser import SystemBrowser
from jarvis.adapters.music import LibraryMusicPlayer
from jarvis.adapters.news import NewsApiReader, NewsConfigurationError, NewsServiceError
from jarvis.core.ports import NewsReader
from jarvis.core.router import parse_command
from jarvis.core.service import AssistantService, ResultStatus


class UnavailableNewsReader:
    """Report missing configuration through the normal service boundary."""

    def headlines(self, *, country: str) -> tuple[str, ...]:
        del country
        raise NewsConfigurationError("NEWS_API_KEY is not configured.")


def create_service() -> AssistantService:
    api_key = os.getenv("NEWS_API_KEY", "")
    news: NewsReader = NewsApiReader(api_key) if api_key else UnavailableNewsReader()
    return AssistantService(
        browser=SystemBrowser(),
        news=news,
        music=LibraryMusicPlayer(musicLibrary.music),
    )


def main() -> int:
    service = create_service()
    print("JARVIS text mode. Enter 'quit' to exit.")

    while True:
        try:
            text = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if text.strip().casefold() in {"quit", "exit"}:
            return 0

        try:
            result = service.execute(parse_command(text))
        except (NewsConfigurationError, NewsServiceError) as error:
            print(f"error: {error}", file=sys.stderr)
            continue

        print(result.message)
        for item in result.payload:
            print(f"- {item}")
        if result.status is ResultStatus.FAILED:
            print("The requested action was not completed.", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())

