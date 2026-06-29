import pytest
from jarvis.core.router import CommandRouter
from jarvis.core.plugin import Plugin

class DummyPlugin(Plugin):
    @property
    def name(self) -> str:
        return "DummyPlugin"

    def can_handle(self, query: str) -> bool:
        return "dummy" in query.lower()

    def execute(self, query: str) -> str:
        return "Executed dummy."

def test_router_handles_valid_command():
    router = CommandRouter()
    router.register_plugin(DummyPlugin())
    response = router.route("run dummy command")
    assert response == "Executed dummy."

def test_router_handles_unknown_command():
    router = CommandRouter()
    router.register_plugin(DummyPlugin())
    response = router.route("do something else")
    assert response == "I'm sorry, I don't know how to handle that command."
