"""Ports implemented by infrastructure adapters."""

from collections.abc import Sequence
from typing import Protocol


class Browser(Protocol):
    """Open an approved URL in the user's browser."""

    def open(self, url: str) -> bool:
        """Return whether the OS accepted the request."""


class NewsReader(Protocol):
    """Retrieve human-readable headlines."""

    def headlines(self, *, country: str) -> Sequence[str]:
        """Return headlines for an ISO 3166-1 alpha-2 country code."""


class MusicPlayer(Protocol):
    """Play a song selected by its normalized library name."""

    def play(self, song: str) -> bool:
        """Return whether playback was started."""

