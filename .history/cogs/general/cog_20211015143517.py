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

    @command(name="fact")
    async def animal_fact(self, ctx, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(title=f"{animal.title()} fact",
                                  description=data["fact"],
                                  colour=ctx.author.colour)
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)
                    await ctx.message.delete()

                else:
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            await ctx.send("No facts are available for that animal.")

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
         name="pick",
        description='For when you wanna settle the score some other way'
    )
    async def pick(ctx, *choices: str):
            await ctx.send(random.choice(choices))

    @commands.command(
         name="repeat",
        description="Repeat a message a number of times."
    )
    async def repeat(ctx, times: int, content='repeating...'):
            for i in range(times):
                await ctx.send(content)

    @commands.command(name="joke")
    async def joke(self, ctx):
        selectjoke = random.choice([
            "Why don’t crabs give to charity? Because they’re shellfish.",
            "Why did the man name his dogs Rolex and Timex? Because they were watch dogs.",
            "My kid wants to invent a pencil with an eraser on each end, but I just don’t see the point."
        ])
        await ctx.send(selectjoke)

    @commands.command(name="coinflip")
    async def coinflip(self, ctx):
        await ctx.send("Heads" if random.randint(1, 2) == 1 else "Tails")

    @commands.command(name="mirror")
    async def mirror(self, ctx, message):
        await ctx.send(message)

    @commands.command(name="wiki")
    @commands.guild_only()
    async def wiki(self, ctx, msg):
        """Get info from wikipedia."""
        url: str = f"https://wikipedia.org/wiki/{msg}"
        await ctx.send(f"Here : {url}")

    @commands.command(name="length")
    async def length(self, ctx, sent):
        sentence: str = ctx.message.content[7:]
        print(sentence)
        length: int = len(sentence)
        i = 0
        count: int = 0
        while i < length - 1:
            i += 1
            if sentence[i] == " ":
                count += 1
        word = count + 1
        letter = i + 1
        await ctx.send(f"World count : {word}, letter count : {letter}")

    @commands.command(name="tableflip")
    async def tableflip(self, ctx):
        # I hope this unicode doesn't break
        """(╯°□°）╯︵ ┻━┻"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=nextcord.File("assets/imgs/reactions/tableflip.gif"))

    @commands.command(name="unflip")
    async def unflip(self, ctx):
        # I hope this unicode doesn't break
        """┬─┬﻿ ノ( ゜-゜ノ)"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=nextcord.File("assets/imgs/reactions/unflip.gif"))

    @commands.command(name="triggered")
    async def triggered(self, ctx):
        """*TRIGGERED*"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=nextcord.File("assets/imgs/reactions/triggered.gif"))

    @commands.command(name="delet")
    async def delet(self, ctx):
        """Delet this"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=nextcord.File("assets/imgs/reactions/delet_this.png"))

    @commands.command(name="weirdshit")
    async def weirdshit(self, ctx):
        """WHY ARE YOU POSTING WEIRD SHIT?!?!?!"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=nextcord.File("assets/imgs/reactions/weirdshit.jpg"))

    @commands.command(name="filth")
    async def filth(self, ctx):
        """THIS IS ABSOLUTELY FILTHY!"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=nextcord.File("assets/imgs/reactions/filth.gif"))

    @commands.command(name="heckoff")
    async def heckoff(self, ctx):
        """heck off fools"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=nextcord.File("assets/imgs/reactions/heckoff.png"))

    @commands.command(name="repost")
    async def repost(self, ctx):
        """It's just a repost smh"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=nextcord.File("assets/imgs/reactions/repost.gif"))

    @commands.command(name="boi")
    async def boi(self, ctx):
        """BOI"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=nextcord.File("assets/imgs/reactions/boi.jpg"))

def setup(bot: commands.Bot):
    bot.add_cog(GeneralCog(bot))
