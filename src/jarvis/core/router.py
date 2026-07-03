import logging

from jarvis.core.plugin import Plugin

logger = logging.getLogger(__name__)


class CommandRouter:
    """Routes commands to the appropriate plugin."""

    def __init__(self, plugins: list[Plugin] | None = None):
        self.plugins = plugins or []

    def register_plugin(self, plugin: Plugin) -> None:
        """Registers a new plugin with the router."""
        self.plugins.append(plugin)
        logger.debug(f"Registered plugin: {plugin.name}")

    def match(self, query: str) -> Plugin | None:
        """Finds the first plugin that can handle the query."""
        logger.info(f"Matching query: '{query}'")
        
        # Sort by priority ascending (lower numbers execute first)
        sorted_plugins = sorted(self.plugins, key=lambda p: p.priority)
        
        for plugin in sorted_plugins:
            if plugin.can_handle(query):
                logger.info(f"Matched plugin {plugin.name} for query.")
                return plugin
        return None
