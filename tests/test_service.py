"""Unit tests for command execution through fake infrastructure ports."""

from dataclasses import dataclass, field

from jarvis.core.models import Action, Command
from jarvis.core.service import AssistantService, ResultStatus


@dataclass
class FakeBrowser:
    accepted: bool = True
    opened: list[str] = field(default_factory=list)

    def open(self, url: str) -> bool:
        self.opened.append(url)
        return self.accepted


@dataclass
class FakeNewsReader:
    values: tuple[str, ...] = ()
    requested_countries: list[str] = field(default_factory=list)

    def headlines(self, *, country: str) -> tuple[str, ...]:
        self.requested_countries.append(country)
        return self.values


@dataclass
class FakeMusicPlayer:
    accepted: bool = True
    played: list[str] = field(default_factory=list)

    def play(self, song: str) -> bool:
        self.played.append(song)
        return self.accepted


def create_service(
    *,
    browser: FakeBrowser | None = None,
    news: FakeNewsReader | None = None,
    music: FakeMusicPlayer | None = None,
) -> AssistantService:
    return AssistantService(
        browser=browser or FakeBrowser(),
        news=news or FakeNewsReader(),
        music=music or FakeMusicPlayer(),
    )


def test_executes_allowlisted_browser_action() -> None:
    browser = FakeBrowser()
    service = create_service(browser=browser)

    result = service.execute(
        Command(Action.OPEN_URL, {"url": "https://google.com"}, "open google")
    )

    assert result.status is ResultStatus.SUCCESS
    assert browser.opened == ["https://google.com"]


def test_encodes_search_query() -> None:
    browser = FakeBrowser()
    service = create_service(browser=browser)

    service.execute(Command(Action.SEARCH_WEB, {"query": "python ports & adapters"}))

    assert browser.opened == [
        "https://www.google.com/search?q=python+ports+%26+adapters"
    ]


def test_returns_news_as_payload() -> None:
    news = FakeNewsReader(("First", "Second"))
    service = create_service(news=news)

    result = service.execute(Command(Action.GET_NEWS))

    assert result.status is ResultStatus.SUCCESS
    assert result.payload == ("First", "Second")
    assert news.requested_countries == ["in"]


def test_unknown_song_is_not_success() -> None:
    music = FakeMusicPlayer(accepted=False)
    service = create_service(music=music)

    result = service.execute(Command(Action.PLAY_MUSIC, {"song": "missing"}))

    assert result.status is ResultStatus.NOT_FOUND
    assert music.played == ["missing"]


def test_unknown_command_has_no_side_effects() -> None:
    browser = FakeBrowser()
    news = FakeNewsReader()
    music = FakeMusicPlayer()
    service = create_service(browser=browser, news=news, music=music)

    result = service.execute(Command(Action.UNKNOWN))

    assert result.status is ResultStatus.UNSUPPORTED
    assert browser.opened == []
    assert news.requested_countries == []
    assert music.played == []

