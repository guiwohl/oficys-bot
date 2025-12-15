import asyncio

from bot import run_bot
from logging_config import configure_logging


def main() -> None:
    configure_logging()
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()
