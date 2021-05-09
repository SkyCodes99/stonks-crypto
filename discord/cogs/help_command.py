import json
import os
import pathlib

import discord
import helpers
from discord.ext import commands
from discord.ext.commands.core import command
from discord.ext.commands.errors import *


ABS_PATH = pathlib.Path(__file__).parent.parent.absolute()

class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(brief="Lists commands and gives info.", usage="help *command")
    async def help(self, ctx, request=None):
        prefix = self.client.command_prefix(self.client, ctx.message)
        if not request:
            embed = helpers.make_embed(title="Commands")
            commands_list = [(name, [command for command in cog.get_commands() if not command.hidden]) for name, cog in self.client.cogs.items()]
            for name, cog_commands in commands_list:
                if len(cog_commands) != 0:
                    embed.add_field(
                        name=name,
                        value='\n'.join([f'`{prefix}`{command}' for command in cog_commands]),
                        inline=True
                        )
        else:
            com = self.client.get_command(request)
            if not com:
                await ctx.send(f"Command '{request}' doesn't exist")
                return
            embed = helpers.make_embed(title=com.name, description=com.brief, footer="* optional")                       
            embed.add_field(name='Usage:', value='`'+prefix+com.usage+'`')
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def kill(self, ctx: commands.Context):
        self.client.remove_cog('handlers')
        await self.client.logout()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: commands.Context, prefix: str):
        with open(os.path.join(ABS_PATH, 'prefixes.json'), 'r', encoding='utf-8') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open(os.path.join(ABS_PATH, 'prefixes.json'), 'w', encoding='utf-8') as f:
            json.dump(prefixes, f)


def setup(client):
    client.add_cog(Help(client))
