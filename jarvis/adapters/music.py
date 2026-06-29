"""Adapter for the legacy static music dictionary."""

import webbrowser
from collections.abc import Mapping


class LibraryMusicPlayer:
    """Open URL-backed songs while rejecting machine-specific local paths."""

    def __init__(self, library: Mapping[str, str]) -> None:
        self._library = library

    def play(self, song: str) -> bool:
        location = self._library.get(song)
        if location is None or not location.startswith(("https://", "http://")):
            return False
        return webbrowser.open(location, new=2)

