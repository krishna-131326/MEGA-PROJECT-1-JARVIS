"""Standard-library browser adapter."""

import webbrowser


class SystemBrowser:
    """Delegate safe URLs from the core to the operating system."""

    def open(self, url: str) -> bool:
        return webbrowser.open(url, new=2)

