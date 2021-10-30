import nextcord
from nextcord.ext import commands

class Reactions(commands.Cog, name="Reactions"):
    """Reaction commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
    bot.add_cog(Reactions(bot))