import discord
import helpers  # type: ignore (pylance)
from discord.ext import commands
from discord.ext.commands.errors import *


class Stocks(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command()
    async def price(self, ctx: commands.Context, *, ticker: str):
        ticker = helpers.Ticker(ticker)
        info = ticker.info
        embed: discord.Embed = helpers.make_embed(title=info.get('shortName'), description=f"${ticker.price}")
        embed.set_thumbnail(url=info["logo_url"])
        await ctx.send(embed=embed)

    @price.error
    async def price_error(self, ctx, error):
        if isinstance(error, (IndexError, CommandInvokeError)):
            await ctx.send("Could not find symbol")
        else:
            raise error


def setup(client: commands.Bot):
    client.add_cog(Stocks(client))
