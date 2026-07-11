import asyncio
import logging

from jarvis.api.dependencies import get_assistant
from jarvis.core.config import settings

logging.basicConfig(
    level=settings.log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def async_main() -> None:
    print("Initializing Jarvis Assistant...")
    assistant = get_assistant()

    print("Type your commands (or 'exit' to quit):")
    while True:
        try:
            command = input(">> ")
            if command.lower() in ("exit", "quit"):
                break

            response_text, _ = await assistant.process(command)
            print(f"Jarvis: {response_text}")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
