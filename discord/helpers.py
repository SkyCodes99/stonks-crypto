from datetime import datetime
from typing import Dict

import discord
import pathlib
import yfinance as yf
import os


ABS_PATH = pathlib.Path(__file__).parent.absolute()
COG_FOLDER = os.path.join(ABS_PATH, 'cogs')
BULLISH = '<:bullish:841477499857797130>'
BEARISH = '<:bearish:841477754658095124>'

def make_embed(title=None, description=None, color=None, author=None,
               image=None, link=None, footer=None) -> discord.Embed:
    """Wrapper for making discord embeds"""
    arg = lambda x: x if x else discord.Embed.Empty
    embed = discord.Embed(
        title=arg(title),
        description=arg(description),
        url=arg(link),
        color=color if color else discord.Color.random()
    )
    if author: embed.set_author(name=author)
    if image: embed.set_image(url=image)
    if footer: embed.set_footer(text=footer)
    else: embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
    return embed

def round_to_hundredth(num: float) -> float:
    return int(num*100) / 100

class Ticker(yf.Ticker):
    def __init__(self, ticker, session=None):
        super().__init__(ticker, session=session)
        self.data = self.info

    @property
    def price(self) -> float:
        return self.history(debug=False, rounding=True).tail(1)['Close'].iloc[0]

    def change(self) -> Dict[str, float]:
        old = self.info['previousClose']
        current = self.price
        return {
            'amount': round_to_hundredth(current-old),
            'percent': round_to_hundredth(((current-old)/old)*100)
        }