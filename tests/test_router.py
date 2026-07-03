import pytest
from jarvis.core.router import CommandRouter
from jarvis.plugins.news_plugin import NewsPlugin

def test_router_handles_valid_command():
    router = CommandRouter()
    plugin = NewsPlugin()
    router.register_plugin(plugin)
    matched = router.match("what's the news")
    assert matched == plugin

def test_router_handles_unknown_command():
    router = CommandRouter()
    router.register_plugin(NewsPlugin())
    matched = router.match("unknown command")
    assert matched is None

class HighPriorityPlugin:
    name = "high"
    priority = 10
    def can_handle(self, query): return True
    
class LowPriorityPlugin:
    name = "low"
    priority = 100
    def can_handle(self, query): return True

def test_router_priority():
    router = CommandRouter()
    # Register in reverse priority order
    router.register_plugin(LowPriorityPlugin())
    router.register_plugin(HighPriorityPlugin())
    
    # High priority should win even if registered last
    matched = router.match("anything")
    assert matched.name == "high"
