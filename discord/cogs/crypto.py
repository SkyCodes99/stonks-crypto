import discord
from discord.ext import commands
from typing import List
from pycoingecko import CoinGeckoAPI


class Crypto(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.cg = CoinGeckoAPI()

def setup(client: commands.Bot):
    client.add_cog(Crypto)

cg = CoinGeckoAPI()
def get_price(ids: List[str], **kwargs):
    return cg.get_price(ids=ids, vs_currencies='usd', **kwargs)

# print(cg.get_coin_by_id('bitcoin', localization=False))
import json

coins_dict = {coin['symbol']: coin['id'] for coin in cg.get_coins_list()}

with open('symbols.json', 'w', encoding='utf-8') as f:
    json.dump(coins_dict, f)