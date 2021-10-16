from random import choice, randint
from typing import Optional
import os
import time
import csv
import re
import asyncio
import platform
import random
import nextcord
from aiohttp import request
from nextcord import Member, Embed
from nextcord.ext.commands import Cog, BucketType
from nextcord.ext.commands import BadArgument
from nextcord.ext.commands import command, cooldown
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

    @command(
         name="slap", 
        aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")
        await ctx.message.delete()

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I can't find that member.")
   
    @commands.command(
        name="echo",
        description="A simple command that repeats the users input back to them.",
    )
    async def echo(self, ctx):
        await ctx.message.delete()
        embed = nextcord.Embed(
            title="Please tell me what you want me to repeat!",
            description="This request will timeout after 1 minute.",
        )
        sent = await ctx.send(embed=embed)

        try:
            msg = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author
                and message.channel == ctx.channel,
            )
            if msg:
                await sent.delete()
                await msg.delete()
                await ctx.send(msg.content)
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelling", delete_after=10)



    @commands.command(
        name="stats", 
          description="A useful command that displays bot statistics."
    )
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = nextcord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        version = "v1.0.0"
        developer = "<@741118153299591240>"
  
        embed = nextcord.Embed(
            title=f"{self.bot.user.name} Stats",
            description="Useful stats.",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Bot Version:", value=version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="nextcord Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value=developer)

        embed.set_footer(text=f"{ctx.author.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)

        await ctx.send(embed=embed)

    @commands.command(name="add", descripton="Adds two numbers together.")
    async def add(ctx, left: int, right: int):
            await ctx.send(left + right)

    @commands.command(
         name="repeat",
        description="Repeat a message a number of times."
    )
    async def repeat(ctx, times: int, content='repeating...'):
            for i in range(times):
                await ctx.send(content)





def setup(bot: commands.Bot):
    bot.add_cog(GeneralCog(bot))
