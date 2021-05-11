import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import json


class Handlers(commands.Cog, name='handlers'):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.client.user.name + " is ready")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if hasattr(ctx.command, 'on_error'):
            return
        ignored = (MissingPermissions, )
        if isinstance(error, CommandNotFound):
            await self.client.get_command('help')(ctx)

        elif isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await self.client.get_command('help')(ctx, ctx.command.name)

        elif isinstance(error, (UserNotFound, MemberNotFound)):
            await ctx.send(f"Member, `{error.argument}`, was not found.")
            
        else:
            raise error

def setup(client: commands.Bot):
    client.add_cog(Handlers(client))