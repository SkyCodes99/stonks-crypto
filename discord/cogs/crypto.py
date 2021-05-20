import discord
from discord.ext import commands
from typing import List
from pycoingecko import CoinGeckoAPI
# from helpers import *  # type: ignore (pylance)


class Crypto(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.cg = CoinGeckoAPI()

def setup(client: commands.Bot):
    client.add_cog(Crypto)


import json
import importlib.util

spec = importlib.util.spec_from_file_location('helpers', './discord/helpers.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)

class Currency():
    cg = CoinGeckoAPI()

    def __init__(self, ticker_or_name: str) -> None:
        self.name = n if (n:=self.symbol_to_id(ticker_or_name)) else ticker_or_name

    @staticmethod
    def symbol_to_id(symbol: str):
        with open(helpers.COG_FOLDER+'/symbols.json', 'r', encoding='utf-8') as f:  # type: ignore (pylance)
            return json.load(f).get(symbol)

    @property
    def price(self) -> int:
        return self.cg.get_price(ids=self.name, vs_currencies='usd')[self.name]['usd']

btc = Currency('btc')
print(btc.name)
print(btc.price)