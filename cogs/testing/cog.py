import random
from typing import Optional

import nextcord
from aiohttp import request
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import BadArgument


class Testing(commands.Cog, name="Testing"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.command(name="say")
	@commands.is_owner()
	async def say(self, ctx, channel:nextcord.TextChannel, *, message):
		if channel is not None:
			await channel.send(message)
     
def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))
