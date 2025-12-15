import random
from typing import Any

from discord.ext import commands

from ui import error, info


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _bump(self, ctx: commands.Context[Any], name: str) -> None:
        await self.bot.store.increment_stat(ctx.author.id, name)

    @commands.command(name="flip")
    async def flip(self, ctx: commands.Context[Any], *options: str):
        """Pick a random option from 2+ choices."""
        if len(options) < 2:
            e = error(
                "Faltam opções",
                "Me dê **pelo menos 2** opções.\n\nExemplo:\n` &flip jogar dormir comer filme `",
            )
            await ctx.send(embed=e)
            return
        await self._bump(ctx, "flip")
        choice = random.choice(options)
        e = info(
            "Escolha aleatória",
            f"Eu girei a roleta e caiu em:\n\n**{choice}**",
            seed="flip",
        )
        e.add_field(name="Opções", value=" • " + " • ".join(options[:20]), inline=False)
        if len(options) > 20:
            e.add_field(name="Nota", value=f"Mostrando 20/{len(options)} opções.", inline=False)
        await ctx.send(embed=e)

    @commands.command(name="coin")
    async def coin(self, ctx: commands.Context[Any]):
        """Simple heads or tails."""
        await self._bump(ctx, "coin")
        result = random.choice(["cara", "coroa"])
        icon = "🪙" if result == "cara" else "🟤"
        e = info("Cara ou coroa", f"{icon} Deu **{result.upper()}**!", seed="coin")
        await ctx.send(embed=e)

    @commands.command(name="roll")
    async def roll(self, ctx: commands.Context[Any], sides: int):
        """Roll a number between 1 and N."""
        if sides < 1:
            e = error("Número inválido", "Use um número **maior que 0**.\nEx: `&roll 20`")
            await ctx.send(embed=e)
            return
        await self._bump(ctx, "roll")
        value = random.randint(1, sides)
        e = info("Dado rolado", f"🎲 **{value}** (1–{sides})", seed=f"roll:{sides}")
        await ctx.send(embed=e)

    @commands.command(name="8ball", aliases=["eightball"])
    async def eight_ball(self, ctx: commands.Context[Any], *question: str):
        """Magic 8-ball style responses."""
        if not question:
            e = error("Cadê a pergunta?", "Exemplo:\n` &8ball vou treinar hoje? `")
            await ctx.send(embed=e)
            return
        responses = [
            "sim",
            "não",
            "talvez",
            "provavelmente",
            "sem chance",
            "fale novamente",
            "parece bom",
            "melhor não dizer agora",
        ]
        await self._bump(ctx, "8ball")
        q = " ".join(question).strip()
        a = random.choice(responses)
        e = info("Bola 8 respondeu", f"**Pergunta:** {q}\n**Resposta:** **{a.upper()}**", seed=q)
        await ctx.send(embed=e)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
