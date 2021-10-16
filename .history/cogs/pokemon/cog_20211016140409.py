import nextcord
import random
from typing import Optional
from aiohttp import request
from nextcord.ext import commands
from nextcord import Member, Embed
from nextcord.ext.commands import BadArgument
class Random(commands.Cog, name="Random"):
	"""Returns random results"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot       

	@commands.command(name="type")
	async def type(self, ctx):
		"""Type advantages."""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/info/weakness.jpg"))
  
def setup(bot: commands.Bot):
	bot.add_cog(Random(bot))