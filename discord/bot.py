import json
import os
import pathlib

import yaml

import discord
from discord.ext import commands


ABS_PATH = pathlib.Path(__file__).parent.absolute()
COG_FOLDER = os.path.join(ABS_PATH, 'cogs')
DEFAULT_PREFIX='$'

def command_prefix(client: commands.Bot, message: discord.Message):
    with open(os.path.join(ABS_PATH, 'prefixes.json'), 'r', encoding='utf-8') as f:
        prefixes = json.load(f)
    if (prefix:=prefixes.get(str(message.guild.id))):
        return prefix
    with open(os.path.join(ABS_PATH, 'prefixes.json'), 'w', encoding='utf-8') as f:
        prefixes[str(message.guild.id)] = '$'
        json.dump(prefixes, f)
    return '$'


intents = discord.Intents.all()
client = commands.Bot(command_prefix=command_prefix, owner_ids=[640393413425889314, 516206994718326795], intents=intents)

client.remove_command('help')

for filename in os.listdir(COG_FOLDER):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


if __name__ == '__main__':
    with open(os.path.join(ABS_PATH, 'config.yaml')) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    client.run(config['bot']['token'])
"febfuibewuifbryuierbfueibfyrueibfeyruifbryeuifbryeifbreuibfyruei"
