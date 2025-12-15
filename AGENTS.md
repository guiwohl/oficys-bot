# Repository Guidelines

## Project Structure & Module Organization

- `bot/`: main source code (Discord bot entrypoints, cogs, storage, UI helpers).
  - `bot/main.py`: starts logging + runs the bot.
  - `bot/bot.py`: `commands.Bot` subclass, loads extensions from `bot/cogs/`.
  - `bot/cogs/`: command modules (e.g., `fun.py`, `games.py`, `time.py`, `meta.py`).
  - `bot/storage/`: persistence layer (`json_store.py` writes `bot/data/store.json`).
  - `bot/data/`: local runtime data (gitignored).
- `run_bot.sh`: convenience script to install deps and run locally.
- `md/`: design/notes docs (not required for runtime).

## Build, Test, and Development Commands

- `./run_bot.sh --install`: installs Python deps from `bot/requirements.txt`, then starts the bot.
- `./run_bot.sh`: starts the bot (expects deps already installed).
- `python bot/main.py`: direct run (same behavior as the script without auto-install).
- `python -m compileall bot`: quick syntax sanity check (useful before opening a PR).

## Coding Style & Naming Conventions

- Language: Python. Use 4-space indentation and keep code close to PEP 8.
- Prefer type hints (the codebase already uses them in cogs and bot lifecycle).
- Naming:
  - Modules/files: `snake_case.py` (e.g., `json_store.py`).
  - Classes: `PascalCase` (e.g., `OficysBot`, `JsonStore`).
  - Commands: keep user-facing command names stable (see `@commands.command(name="...")`).
- No formatter/linter is enforced in-repo currently; keep diffs small and consistent.

## Testing Guidelines

This repo does not include an automated test suite yet. For changes:
- Run `python -m compileall bot`.
- Smoke test by running the bot and exercising the changed command(s) in a Discord server.

## Commit & Pull Request Guidelines

- Git history is minimal (no established convention). Use short, imperative summaries (e.g., “Add stats embed”).
- PRs should include:
  - What changed + why (brief).
  - How to test (exact commands and example Discord messages like `&gameshow >7`).
  - Notes on behavior changes and any new env vars/dependencies.

## Security & Configuration Tips

- Never commit secrets: `bot/.env` is gitignored. If a token leaks, rotate it in the Discord Developer Portal.
- The bot relies on **Message Content Intent** for prefix commands; ensure it’s enabled when deploying.

