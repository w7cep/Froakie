from random import choice
from typing import Optional
import asyncio
import platform
import nextcord
from nextcord import Member
from nextcord.ext.commands import BadArgument
from nextcord.ext.commands import command
from nextcord.ext import commands

class GeneralCog(commands.Cog, name="General"):
    """General commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None
        
    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!")

    @command(name="bye")
    async def say_bye(self, ctx):
        await ctx.send(f"{choice(('Bye', 'Peace', 'See Ya', 'Later'))} {ctx.author.mention}!")

def setup(bot: commands.Bot):
    bot.add_cog(GeneralCog(bot))
