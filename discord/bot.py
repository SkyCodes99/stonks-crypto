import discord
from discord.ext import commands
import os
import yaml


PREFIX = '$'
intents = discord.Intents.all()
client = commands.Bot(command_prefix=PREFIX, owner_ids=[640393413425889314, 516206994718326795], intents=intents)

client.remove_command('help')

COG_FOLDER = './discord/cogs'
for filename in os.listdir(COG_FOLDER):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


if __name__ == '__main__':
    with open('./discord/config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        print(config)
    client.run(config['bot']['token'])