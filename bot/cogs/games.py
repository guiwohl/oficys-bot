from typing import Any, Optional, Tuple

from discord.ext import commands

from ui import error, format_filter, info, success


def parse_filter(arg: Optional[str]) -> Tuple[Optional[str], Optional[int]]:
    if not arg:
        return None, None
    if len(arg) < 2:
        return None, None
    comparator, number = arg[0], arg[1:]
    if comparator not in {">", "<"}:
        return None, None
    if not number.isdigit():
        return None, None
    return comparator, int(number)


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _bump(self, ctx: commands.Context[Any], name: str) -> None:
        await self.bot.store.increment_stat(ctx.author.id, name)

    @commands.command(name="gamedump")
    async def gamedump(self, ctx: commands.Context[Any], *, body: str):
        """Save or update a game with rating."""
        parts = body.split()
        if len(parts) < 2 or not parts[-1].isdigit():
            e = error(
                "Formato inválido",
                "Use:\n` &gamedump <nome do jogo> <0-10> `\n\nExemplos:\n` &gamedump Minecraft 8 `\n` &gamedump The Witcher 3 10 `",
            )
            await ctx.send(embed=e)
            return
        rating = int(parts[-1])
        if rating < 0 or rating > 10:
            await ctx.send(embed=error("Nota inválida", "A nota precisa ser entre **0** e **10**."))
            return
        game_name = " ".join(parts[:-1]).strip()
        if not game_name:
            await ctx.send(embed=error("Sem nome do jogo", "Escreva o nome do jogo antes da nota."))
            return
        await self.bot.store.add_or_update_game(ctx.author.id, game_name, rating)
        await self._bump(ctx, "gamedump")
        stars = "⭐" * max(1, min(10, rating))
        e = success(
            "Jogo salvo!",
            f"**{game_name}**\nNota: **{rating}/10**  {stars}",
        )
        e.add_field(name="Próximo passo", value="Veja sua lista com `&gameshow` ou peça um aleatório com `&randomgame`.", inline=False)
        await ctx.send(embed=e)

    @commands.command(name="gameshow")
    async def gameshow(self, ctx: commands.Context[Any], filter_by: Optional[str] = None):
        """Show saved games, optionally filtered by rating."""
        comparator, threshold = parse_filter(filter_by)
        games = await self.bot.store.list_games(ctx.author.id, comparator, threshold)
        await self._bump(ctx, "gameshow")
        if not games:
            e = info("Sua lista está vazia", f"Nenhum jogo encontrado ({format_filter(filter_by)}).\n\nDica: salve um jogo com `&gamedump`.")
            await ctx.send(embed=e)
            return
        games_sorted = sorted(games, key=lambda g: (g.get("rating", 0), g.get("game_name", "")), reverse=True)

        shown = games_sorted[:20]
        rest = len(games_sorted) - len(shown)
        lines = [f"**{g['game_name']}** — `{g['rating']}/10`" for g in shown]

        title = "🎮 Seus jogos salvos"
        desc = f"{format_filter(filter_by)}\n\n" + "\n".join(f"• {line}" for line in lines)
        if rest > 0:
            desc += f"\n\n… e mais **{rest}** jogo(s). (Vou precisar de paginação pra listar tudo.)"

        e = info(title, desc, seed=f"gameshow:{filter_by}")
        e.add_field(name="Total", value=str(len(games_sorted)), inline=True)
        e.add_field(name="Dica", value="Use `&randomgame >7` pra pegar só os bem avaliados.", inline=True)
        await ctx.send(embed=e)

    @commands.command(name="randomgame")
    async def randomgame(self, ctx: commands.Context[Any], filter_by: Optional[str] = None):
        """Pick a random game from saved list."""
        comparator, threshold = parse_filter(filter_by)
        game = await self.bot.store.random_game(ctx.author.id, comparator, threshold)
        await self._bump(ctx, "randomgame")
        if not game:
            e = info("Nada encontrado", f"Não achei nenhum jogo para escolher ({format_filter(filter_by)}).\n\nDica: tente `&gameshow`.")
            await ctx.send(embed=e)
            return
        rating = game["rating"]
        stars = "⭐" * max(1, min(10, rating))
        e = info(
            "Sugestão aleatória",
            f"Hoje a recomendação é:\n\n**{game['game_name']}**\nNota salva: **{rating}/10**  {stars}",
            seed=f"random:{game['game_name']}",
        )
        e.add_field(name="Filtro", value=format_filter(filter_by), inline=True)
        e.add_field(name="Quer trocar?", value="Rode de novo: `&randomgame`", inline=True)
        await ctx.send(embed=e)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Games(bot))
