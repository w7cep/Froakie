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
	
def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))
