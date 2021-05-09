import os
import pathlib

import yaml

import discord
from discord.ext import commands

ABS_PATH = pathlib.Path(__file__).parent.absolute()
COG_FOLDER = os.path.join(ABS_PATH, 'cogs')

def command_prefix(message, client):
    return '$'


intents = discord.Intents.all()
client = commands.Bot(command_prefix='command_prefix', owner_ids=[640393413425889314, 516206994718326795], intents=intents)

client.remove_command('help')

for filename in os.listdir(COG_FOLDER):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


if __name__ == '__main__':
    with open('./discord/config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    client.run(config['bot']['token'])
