import logging

from jarvis.core.config import settings
from jarvis.core.router import CommandRouter
from jarvis.plugins.browser_plugin import BrowserPlugin
from jarvis.plugins.music_plugin import MusicPlugin
from jarvis.plugins.news_plugin import NewsPlugin
from jarvis.providers.music_provider import WebMusicProvider

logging.basicConfig(
    level=settings.log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def get_router() -> CommandRouter:
    router = CommandRouter()

    # Initialize providers
    music_provider = WebMusicProvider(config_path=settings.music_config_path)
    # llm_provider = GrokProvider(api_key=settings.grok_api_key)

    # Register plugins
    router.register_plugin(NewsPlugin())
    router.register_plugin(BrowserPlugin())
    router.register_plugin(MusicPlugin(provider=music_provider))

    return router


def main() -> None:
    print("Initializing Jarvis Assistant...")
    router = get_router()

    print("Type your commands (or 'exit' to quit):")
    while True:
        try:
            command = input(">> ")
            if command.lower() in ("exit", "quit"):
                break

            response = router.route(command)
            print(f"Jarvis: {response}")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
