"""Value objects shared by the assistant core and its adapters."""

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Final, Mapping


class Action(StrEnum):
    """Actions understood by the deterministic command router."""

    OPEN_URL = "open_url"
    PLAY_MUSIC = "play_music"
    SEARCH_WEB = "search_web"
    GET_NEWS = "get_news"
    UNKNOWN = "unknown"


EMPTY_ARGUMENTS: Final[Mapping[str, str]] = MappingProxyType({})


def _empty_arguments() -> Mapping[str, str]:
    return EMPTY_ARGUMENTS


@dataclass(frozen=True, slots=True)
class Command:
    """A normalized, side-effect-free representation of a user request."""

    action: Action
    arguments: Mapping[str, str] = field(default_factory=_empty_arguments)
    raw_text: str = ""
