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

    def route(self, query: str) -> str:
        """Routes the query to the first matching plugin."""
        logger.info(f"Routing query: '{query}'")
        for plugin in self.plugins:
            if plugin.can_handle(query):
                logger.info(f"Plugin {plugin.name} handling query.")
                try:
                    return plugin.execute(query)
                except Exception as e:
                    logger.error(f"Error executing plugin {plugin.name}: {e}")
                    return f"Error executing command via {plugin.name}."

        return "I'm sorry, I don't know how to handle that command."
