import json
import os

import yaml
from helpers import *  # type: ignore (pylance)
import discord
from discord.ext import commands


with open(os.path.join(ABS_PATH, 'config.yaml')) as f:  # type: ignore (pylance)
        config = yaml.load(f, Loader=yaml.FullLoader)
        print(config)
    
DEFAULT_PREFIX = config['bot']['prefix']
TOKEN = config['bot']['token']
OWNER_IDS = config['bot']['owner_ids']

def command_prefix(client: commands.Bot, message: discord.Message):
    user_id = client.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ']
    if message.guild:
        with open(os.path.join(ABS_PATH, 'prefixes.json'), 'r', encoding='utf-8') as f:  # type: ignore (pylance)
            prefixes = json.load(f)

        if (prefix:=prefixes.get(str(message.guild.id))):
            base.insert(0, prefix)
            return base

        with open(os.path.join(ABS_PATH, 'prefixes.json'), 'w', encoding='utf-8') as f:  # type: ignore (pylance)
            prefixes[str(message.guild.id)] = DEFAULT_PREFIX
            json.dump(prefixes, f)
            
    base.insert(0, DEFAULT_PREFIX)
    return base


intents = discord.Intents.all()
client = commands.Bot(
    command_prefix=command_prefix,
    owner_ids=OWNER_IDS,
    intents=intents
)

client.remove_command('help')

for filename in os.listdir(COG_FOLDER):  # type: ignore (pylance)
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    client.run(TOKEN)