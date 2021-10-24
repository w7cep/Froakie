import nextcord
import random
from typing import Optional
from aiohttp import request
from nextcord.ext import commands
from nextcord import Member, Embed
from nextcord.ext.commands import BadArgument

class Testing(commands.Cog, name="Testing"):
	"""Test commands"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="add", descripton="Adds two numbers together.")
	async def add(ctx, left: int, right: int):
			await ctx.send(left + right)

	@commands.command(
		 name="repeat",
		description="Repeat a message a number of times.", hidden=True
	)
	async def repeat(ctx, times: int, content='repeating...'):
			for i in range(times):
				await ctx.send(content)

def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))