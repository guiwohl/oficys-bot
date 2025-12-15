from __future__ import annotations

import random
from typing import Iterable, Optional

import discord


class Theme:
    PRIMARY = discord.Color.blurple()
    SUCCESS = discord.Color.green()
    WARNING = discord.Color.orange()
    ERROR = discord.Color.red()


def _pick_emoji(seed: str) -> str:
    rng = random.Random(seed)
    return rng.choice(["✨", "🌟", "💫", "🎯", "🧠", "⚡", "🪄", "🎲", "🧩"])


def embed(
    *,
    title: str,
    description: str | None = None,
    color: discord.Color = Theme.PRIMARY,
    footer: str | None = "Oficys • digite &help para ver tudo",
) -> discord.Embed:
    e = discord.Embed(title=title, description=description, color=color)
    if footer:
        e.set_footer(text=footer)
    return e


def success(title: str, description: str | None = None) -> discord.Embed:
    return embed(title=f"✅ {title}", description=description, color=Theme.SUCCESS)


def warn(title: str, description: str | None = None) -> discord.Embed:
    return embed(title=f"⚠️ {title}", description=description, color=Theme.WARNING)


def error(title: str, description: str | None = None) -> discord.Embed:
    return embed(title=f"❌ {title}", description=description, color=Theme.ERROR)


def info(title: str, description: str | None = None, *, seed: str | None = None) -> discord.Embed:
    prefix = _pick_emoji(seed or title)
    return embed(title=f"{prefix} {title}", description=description, color=Theme.PRIMARY)


def clamp_fields(items: Iterable[tuple[str, str, bool]], limit: int = 25) -> list[tuple[str, str, bool]]:
    out: list[tuple[str, str, bool]] = []
    for idx, item in enumerate(items):
        if idx >= limit:
            break
        out.append(item)
    return out


def add_fields(e: discord.Embed, items: Iterable[tuple[str, str, bool]]) -> discord.Embed:
    for name, value, inline in items:
        e.add_field(name=name[:256], value=value[:1024] if value else "\u200b", inline=inline)
    return e


def pretty_list(items: list[str], *, bullet: str = "•", max_items: int = 20) -> str:
    if not items:
        return "—"
    shown = items[:max_items]
    rest = len(items) - len(shown)
    text = "\n".join(f"{bullet} {x}" for x in shown)
    if rest > 0:
        text += f"\n… e mais {rest}."
    return text


def format_filter(filter_by: Optional[str]) -> str:
    if not filter_by:
        return "sem filtro"
    return f"filtro: `{filter_by}`"
