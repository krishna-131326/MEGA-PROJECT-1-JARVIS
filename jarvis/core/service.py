"""Application service that executes parsed commands through injected ports."""

from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import urlencode

from jarvis.core.models import Action, Command
from jarvis.core.ports import Browser, MusicPlayer, NewsReader


class ResultStatus(StrEnum):
    """Machine-readable command outcomes."""

    SUCCESS = "success"
    NOT_FOUND = "not_found"
    UNSUPPORTED = "unsupported"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class CommandResult:
    """The observable result of command execution."""

    status: ResultStatus
    message: str
    payload: tuple[str, ...] = ()


@dataclass(slots=True)
class AssistantService:
    """Execute commands while keeping infrastructure dependencies explicit."""

    browser: Browser
    news: NewsReader
    music: MusicPlayer

    def execute(self, command: Command) -> CommandResult:
        if command.action is Action.OPEN_URL:
            return self._open_url(command.arguments["url"])

        if command.action is Action.SEARCH_WEB:
            query = command.arguments["query"]
            url = f"https://www.google.com/search?{urlencode({'q': query})}"
            return self._open_url(url)

        if command.action is Action.PLAY_MUSIC:
            song = command.arguments["song"]
            if self.music.play(song):
                return CommandResult(ResultStatus.SUCCESS, f"Playing {song}.")
            return CommandResult(ResultStatus.NOT_FOUND, f"Song not found: {song}.")

        if command.action is Action.GET_NEWS:
            headlines = tuple(self.news.headlines(country="in"))
            if not headlines:
                return CommandResult(ResultStatus.NOT_FOUND, "No headlines were returned.")
            return CommandResult(
                ResultStatus.SUCCESS,
                f"Retrieved {len(headlines)} headlines.",
                headlines,
            )

        return CommandResult(
            ResultStatus.UNSUPPORTED,
            "I do not understand that command.",
        )

    def _open_url(self, url: str) -> CommandResult:
        if self.browser.open(url):
            return CommandResult(ResultStatus.SUCCESS, f"Opened {url}.")
        return CommandResult(ResultStatus.FAILED, f"The browser rejected {url}.")

