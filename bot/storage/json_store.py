import asyncio
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class JsonStore:
    def __init__(self, path: Path):
        self.path = path
        self._lock = asyncio.Lock()
        self._ensure_file()

    def _ensure_file(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text(json.dumps({"games": [], "command_stats": {}}), encoding="utf-8")

    def _read(self) -> Dict[str, Any]:
        raw = self.path.read_text(encoding="utf-8")
        try:
            data = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            data = {}
        data.setdefault("games", [])
        data.setdefault("command_stats", {})
        return data

    def _write(self, data: Dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    async def add_or_update_game(self, user_id: int, game_name: str, rating: int) -> None:
        async with self._lock:
            data = self._read()
            games: List[Dict[str, Any]] = data["games"]
            updated = False
            for item in games:
                if item["user_id"] == user_id and item["game_name"].lower() == game_name.lower():
                    item["rating"] = rating
                    updated = True
                    break
            if not updated:
                games.append(
                    {
                        "user_id": user_id,
                        "game_name": game_name,
                        "rating": rating,
                        "created_at": int(time.time()),
                    }
                )
            data["games"] = games
            self._write(data)

    async def list_games(self, user_id: int, comparator: Optional[str] = None, threshold: Optional[int] = None) -> List[Dict[str, Any]]:
        async with self._lock:
            data = self._read()
        games = [g for g in data["games"] if g["user_id"] == user_id]
        if comparator and threshold is not None:
            if comparator == ">":
                games = [g for g in games if g["rating"] > threshold]
            elif comparator == "<":
                games = [g for g in games if g["rating"] < threshold]
        return games

    async def random_game(self, user_id: int, comparator: Optional[str] = None, threshold: Optional[int] = None) -> Optional[Dict[str, Any]]:
        games = await self.list_games(user_id, comparator, threshold)
        if not games:
            return None
        import random

        return random.choice(games)

    async def increment_stat(self, user_id: int, command: str) -> None:
        async with self._lock:
            data = self._read()
            stats: Dict[str, Dict[str, int]] = data["command_stats"]
            user_stats = stats.get(str(user_id), {})
            user_stats[command] = user_stats.get(command, 0) + 1
            stats[str(user_id)] = user_stats
            data["command_stats"] = stats
            self._write(data)

    async def get_stats(self, user_id: int) -> Dict[str, int]:
        async with self._lock:
            data = self._read()
        return data["command_stats"].get(str(user_id), {})
