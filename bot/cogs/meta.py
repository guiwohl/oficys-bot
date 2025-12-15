from typing import Any, List, Tuple

from discord.ext import commands

from config import COMMAND_PREFIX
from ui import info


class Meta(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _bump(self, ctx: commands.Context[Any], name: str) -> None:
        await self.bot.store.increment_stat(ctx.author.id, name)

    @commands.command(name="help")
    async def help(self, ctx: commands.Context[Any]):
        await self._bump(ctx, "help")
        e = info(
            "Oficys — Ajuda",
            "Comandos disponíveis (prefixo `&`).\n"
            "Dica: você pode clicar e copiar os exemplos.",
            seed="help",
        )
        e.add_field(name=f"🎯 {COMMAND_PREFIX}flip a b c", value="Escolhe **uma** opção aleatória entre 2+.", inline=False)
        e.add_field(name=f"🪙 {COMMAND_PREFIX}coin", value="Cara ou coroa.", inline=True)
        e.add_field(name=f"🎲 {COMMAND_PREFIX}roll 20", value="Número aleatório de 1 a N.", inline=True)
        e.add_field(name=f"🔮 {COMMAND_PREFIX}8ball vou treinar hoje?", value="Respostas estilo bola 8.", inline=False)

        e.add_field(name=f"🎮 {COMMAND_PREFIX}gamedump Nome do Jogo 8", value="Salva/atualiza jogo + nota (0–10).", inline=False)
        e.add_field(name=f"📚 {COMMAND_PREFIX}gameshow", value="Lista seus jogos (use `>7` / `<7`).", inline=True)
        e.add_field(name=f"🎁 {COMMAND_PREFIX}randomgame >7", value="Escolhe um jogo aleatório (com filtro).", inline=True)

        e.add_field(name=f"⏱️ {COMMAND_PREFIX}now", value="Mostra horário em vários fusos + info do dia.", inline=False)
        e.add_field(name=f"⏳ {COMMAND_PREFIX}countdown 7", value="Contagem regressiva (edita a mensagem).", inline=True)
        e.add_field(name=f"📅 {COMMAND_PREFIX}timeuntil 31/12/2025", value="Quanto falta até uma data.", inline=True)

        e.add_field(name=f"📊 {COMMAND_PREFIX}stats", value="Suas estatísticas de uso.", inline=True)
        e.add_field(name=f"🧭 {COMMAND_PREFIX}help", value="Mostra esta ajuda.", inline=True)
        await ctx.send(embed=e)

    @commands.command(name="stats")
    async def stats(self, ctx: commands.Context[Any]):
        stats = await self.bot.store.get_stats(ctx.author.id)
        await self._bump(ctx, "stats")
        if not stats:
            e = info("Stats", "Você ainda não usou nenhum comando.\n\nComece com `&help` 😉", seed="stats-empty")
            await ctx.send(embed=e)
            return
        ordered: List[Tuple[str, int]] = sorted(stats.items(), key=lambda item: item[1], reverse=True)
        total = sum(count for _, count in ordered)
        top = ordered[:12]
        e = info("Stats", f"📈 Total de comandos usados: **{total}**", seed=f"stats:{ctx.author.id}")
        for name, count in top:
            e.add_field(name=f"• {name}", value=str(count), inline=True)
        await ctx.send(embed=e)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Meta(bot))
