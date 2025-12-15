#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

export PYTHONUNBUFFERED=1

if [[ "${1:-}" == "--install" ]]; then
  python -m pip install -r bot/requirements.txt
  shift
fi

echo "Starting Oficys bot..."
echo "  - LOG_LEVEL=${LOG_LEVEL:-INFO}"
echo "  - DISCORD_LOG_LEVEL=${DISCORD_LOG_LEVEL:-WARNING}"
echo "  - LOG_FILE=${LOG_FILE:-}"
echo

exec python bot/main.py
