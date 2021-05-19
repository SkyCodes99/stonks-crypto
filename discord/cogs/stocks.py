import discord
from helpers import *  # type: ignore (pylance)
from discord.ext import commands
from discord.ext.commands.errors import *


class Stocks(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command(
        aliases=['stock'],
        brief="Check the price of any stock",
        usage="price <symbol>"
    )
    async def price(self, ctx: commands.Context, *, ticker: str):
        ticker = Ticker(ticker)  # type: ignore (pylance)
        info = ticker.info
        change = ticker.change()

        if change['amount'] < 0:
            change['amount'] *= -1
            positive = False
        else:
            positive = True

        embed: discord.Embed = make_embed(  # type: ignore (pylance)
            title=info.get('shortName'),
            description=(f"${ticker.price}\n{BULLISH if positive else BEARISH} " +  # type: ignore (pylance)
                        f"{'-' if not positive else ''}${change['amount']}, " +
                        f"{change['percent']}%"),
            color=discord.Color.green() if positive else discord.Color.red()
        )
        embed.set_thumbnail(url=info["logo_url"])
        await ctx.send(embed=embed)

    @price.error
    async def price_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, (IndexError, CommandInvokeError)):
            await ctx.send("Could not find symbol")
        elif isinstance(error, MissingRequiredArgument):
            await self.client.get_command('help')(ctx, ctx.command.name)
        else:
            raise error


def setup(client: commands.Bot):
    client.add_cog(Stocks(client))
