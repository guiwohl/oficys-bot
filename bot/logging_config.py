import logging
import os
import sys
from datetime import datetime
from typing import Optional


_LEVEL_COLORS: dict[int, str] = {
    logging.DEBUG: "\x1b[38;5;245m",
    logging.INFO: "\x1b[38;5;39m",
    logging.WARNING: "\x1b[38;5;214m",
    logging.ERROR: "\x1b[38;5;196m",
    logging.CRITICAL: "\x1b[1;38;5;196m",
}

_RESET = "\x1b[0m"
_DIM = "\x1b[2m"


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        created = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        level = record.levelname
        logger = record.name
        msg = record.getMessage()

        color = _LEVEL_COLORS.get(record.levelno, "")
        level_colored = f"{color}{level:<8}{_RESET}" if color else f"{level:<8}"
        prefix = f"{_DIM}{created}{_RESET} {level_colored} {_DIM}{logger}{_RESET}"

        if record.exc_info:
            exc = self.formatException(record.exc_info)
            return f"{prefix} {msg}\n{exc}"
        return f"{prefix} {msg}"


def configure_logging(*, level: Optional[str] = None, log_file: Optional[str] = None) -> None:
    """
    Configure console (colored) logging + optional file logging.

    Env vars:
      - LOG_LEVEL: DEBUG|INFO|WARNING|ERROR (default INFO)
      - LOG_FILE: path to a log file (optional)
    """
    chosen_level = (level or os.getenv("LOG_LEVEL") or "INFO").upper()
    chosen_file = log_file or os.getenv("LOG_FILE")

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(chosen_level)

    console = logging.StreamHandler(stream=sys.stdout)
    console.setLevel(chosen_level)
    console.setFormatter(ColorFormatter())
    root.addHandler(console)

    if chosen_file:
        file_handler = logging.FileHandler(chosen_file, encoding="utf-8")
        file_handler.setLevel(chosen_level)
        file_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        root.addHandler(file_handler)

    logging.getLogger("discord").setLevel(os.getenv("DISCORD_LOG_LEVEL", "WARNING").upper())
