import asyncio
import logging
from pathlib import Path

import discord
from discord.ext import commands

from config import COMMAND_PREFIX, get_app_id, get_bot_token
from storage.json_store import JsonStore
from ui import error as error_embed
from ui import warn as warn_embed


BASE_DIR = Path(__file__).resolve().parent
COGS = [
    "cogs.fun",
    "cogs.games",
    "cogs.time",
    "cogs.meta",
]

logger = logging.getLogger("oficys.bot")


class OficysBot(commands.Bot):
    def __init__(self, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=intents,
            help_command=None,
            **kwargs,
        )
        self.store = JsonStore(BASE_DIR / "data" / "store.json")
        self.app_id = get_app_id()

    async def setup_hook(self) -> None:
        logger.info("Loading extensions: %s", ", ".join(COGS))
        for ext in COGS:
            try:
                await self.load_extension(ext)
                logger.info("Loaded extension: %s", ext)
            except Exception:
                logger.exception("Failed to load extension: %s", ext)

        logger.info("Prefix: %s", COMMAND_PREFIX)

    async def on_ready(self) -> None:
        user = self.user
        if user:
            logger.info("Logged in as %s (id=%s)", user, user.id)
        logger.info("Connected guilds: %s", len(self.guilds))

    async def on_command(self, ctx: commands.Context) -> None:
        channel = getattr(ctx.channel, "name", "DM")
        guild = getattr(ctx.guild, "name", "DM")
        logger.info(
            "Command: %s | user=%s(%s) | guild=%s | channel=%s",
            ctx.command.qualified_name if ctx.command else "?",
            ctx.author,
            ctx.author.id,
            guild,
            channel,
        )

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingRequiredArgument):
            usage = f"`{COMMAND_PREFIX}{ctx.command.qualified_name} {ctx.command.signature}`" if ctx.command else "`comando`"
            await ctx.send(
                embed=warn_embed(
                    "Faltou algum argumento",
                    f"Uso correto:\n{usage}\n\nDica: `&help` mostra exemplos.",
                )
            )
            return
        if isinstance(error, commands.BadArgument):
            usage = f"`{COMMAND_PREFIX}{ctx.command.qualified_name} {ctx.command.signature}`" if ctx.command else "`comando`"
            await ctx.send(embed=warn_embed("Argumento inválido", f"Tente assim:\n{usage}"))
            return
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=warn_embed("Calma aí 😅", f"Tente de novo em **{error.retry_after:.1f}s**."))
            return
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=error_embed("Sem permissão", "Você não pode usar esse comando aqui."))
            return

        # Generic fallback for unexpected errors.
        await ctx.send(
            embed=error_embed(
                "Ops, algo deu errado",
                "O erro foi registrado no terminal.\nTente novamente em alguns segundos.",
            )
        )
        logger.exception(
            "Command error: %s | user=%s(%s) | content=%r",
            ctx.command.qualified_name if ctx.command else "?",
            ctx.author,
            ctx.author.id,
            getattr(ctx.message, "content", ""),
            exc_info=error,
        )


async def run_bot() -> None:
    bot = OficysBot()
    async with bot:
        await bot.start(get_bot_token(), reconnect=True)


if __name__ == "__main__":
    asyncio.run(run_bot())
