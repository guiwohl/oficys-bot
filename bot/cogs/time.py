import asyncio
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from discord.ext import commands

from config import MAIN_TIMEZONE, TIMEZONES
from ui import error, info, success


def _day_indicator(now: datetime) -> str:
    symbols = ["S", "T", "Q", "Q", "S", "S", "D"]
    today = now.weekday()  # Monday=0
    parts = []
    for idx, sym in enumerate(symbols):
        if idx == today:
            parts.append(f"**{sym}**")
        else:
            parts.append(sym)
    return "  ".join(parts)


class TimeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _bump(self, ctx: commands.Context[Any], name: str) -> None:
        await self.bot.store.increment_stat(ctx.author.id, name)

    @commands.command(name="now")
    async def now(self, ctx: commands.Context[Any]):
        """Show time in multiple zones plus day info."""
        await self._bump(ctx, "now")
        main = datetime.now(ZoneInfo(MAIN_TIMEZONE))
        day_of_year = main.timetuple().tm_yday
        is_leap = int(datetime(main.year, 12, 31, tzinfo=main.tzinfo).timetuple().tm_yday == 366)
        total_days = 366 if is_leap else 365
        seconds_left = int(
            (datetime(main.year, main.month, main.day, 23, 59, 59, tzinfo=main.tzinfo) - main).total_seconds()
        )
        hours_left = max(0, seconds_left // 3600)

        e = info("Agora", "⏱️ Horários e informações do dia.", seed="now")
        for tz_name in TIMEZONES[:20]:
            tz = ZoneInfo(tz_name)
            current = datetime.now(tz)
            e.add_field(
                name=f"🕒 {tz_name}",
                value=current.strftime("`%H:%M:%S`  •  `%d/%m/%Y`"),
                inline=True,
            )

        e.add_field(
            name="📅 Hoje",
            value=f"{main.strftime('%A')}  ({_day_indicator(main)})",
            inline=False,
        )
        e.add_field(name="📌 Dia do ano", value=f"{day_of_year}/{total_days}", inline=True)
        e.add_field(name="🌙 Horas restantes", value=str(hours_left), inline=True)
        await ctx.send(embed=e)

    @commands.command(name="countdown")
    async def countdown(self, ctx: commands.Context[Any], minutes: int):
        """Countdown in minutes, editing the message every 15 seconds."""
        if minutes <= 0:
            await ctx.send(embed=error("Minutos inválidos", "Use um número **maior que 0**.\nEx: `&countdown 7`"))
            return
        if minutes > 240:
            await ctx.send(embed=error("Muito longo", "Máximo permitido: **240** minutos."))
            return

        total_seconds = minutes * 60
        await self._bump(ctx, "countdown")
        remaining = total_seconds

        def bar(rem: int) -> str:
            total = total_seconds
            done = total - rem
            blocks = 12
            filled = 0 if total == 0 else int((done / total) * blocks)
            filled = max(0, min(blocks, filled))
            return "🟩" * filled + "⬛" * (blocks - filled)

        e = info("Contagem regressiva", f"⏳ Começando: **{minutes}** minuto(s).", seed=f"countdown:{minutes}")
        e.add_field(name="Progresso", value=bar(remaining), inline=False)
        e.add_field(name="Restante", value=f"`{minutes}m 0s`", inline=True)
        e.add_field(name="Atualiza", value="a cada `15s`", inline=True)
        msg = await ctx.send(embed=e)
        try:
            while remaining > 0:
                await asyncio.sleep(15)
                remaining -= 15
                if remaining < 0:
                    remaining = 0
                mins, secs = divmod(remaining, 60)
                e.description = "⏳ Em andamento..."
                e.set_field_at(0, name="Progresso", value=bar(remaining), inline=False)
                e.set_field_at(1, name="Restante", value=f"`{mins}m {secs}s`", inline=True)
                await msg.edit(embed=e)
            end = success("Tempo esgotado!", "⏰ Bora! (Se quiser outra: `&countdown 5`)")
            await msg.edit(embed=end)
        except Exception:
            # Fail silently if message was deleted or edit was blocked.
            return

    @commands.command(name="timeuntil")
    async def timeuntil(self, ctx: commands.Context[Any], *, date_str: str):
        """Time remaining until dd/MM/YYYY."""
        try:
            target_naive = datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            await ctx.send(embed=error("Formato inválido", "Use `dd/MM/YYYY`.\nEx: `&timeuntil 31/12/2025`"))
            return
        now = datetime.now(ZoneInfo(MAIN_TIMEZONE))
        target = datetime(
            target_naive.year,
            target_naive.month,
            target_naive.day,
            tzinfo=ZoneInfo(MAIN_TIMEZONE),
        )
        delta = target - now
        if delta.total_seconds() < 0:
            await ctx.send(embed=error("Essa data já passou", f"Tente uma data no futuro. Ex: `&timeuntil 31/12/{now.year}`"))
            return
        total_seconds = int(delta.total_seconds())
        years = total_seconds // (365 * 24 * 3600)
        rem = total_seconds % (365 * 24 * 3600)
        months = rem // (30 * 24 * 3600)
        rem %= 30 * 24 * 3600
        days = rem // (24 * 3600)
        rem %= 24 * 3600
        hours = rem // 3600
        rem %= 3600
        minutes = rem // 60
        seconds = rem % 60

        await self._bump(ctx, "timeuntil")
        ts = int(target.timestamp())
        e = info("Tempo até a data", f"📍 Alvo: **{date_str}**\n⏳ Relative: <t:{ts}:R>", seed=f"timeuntil:{date_str}")
        e.add_field(name="Anos", value=str(years), inline=True)
        e.add_field(name="Meses", value=str(months), inline=True)
        e.add_field(name="Dias", value=str(days), inline=True)
        e.add_field(name="Horas", value=str(hours), inline=True)
        e.add_field(name="Minutos", value=str(minutes), inline=True)
        e.add_field(name="Segundos", value=str(seconds), inline=True)
        await ctx.send(embed=e)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TimeCog(bot))
