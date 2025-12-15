import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from the .env file located in the project root.
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)


COMMAND_PREFIX = "&"
MAIN_TIMEZONE = "America/Sao_Paulo"
# Additional timezones to display in the `now` command.
TIMEZONES = [
    MAIN_TIMEZONE,
    "UTC",
    "America/New_York",
    "Europe/London",
]


def get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set in the environment.")
    return token


def get_app_id() -> str | None:
    return os.getenv("APP_ID")
