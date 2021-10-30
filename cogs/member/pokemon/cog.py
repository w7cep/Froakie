import nextcord
import random
from typing import Optional
from aiohttp import request
from nextcord.ext import commands
from nextcord import Member, Embed
from nextcord.ext.commands import BadArgument
class Pokemon(commands.Cog, name="Pokemon"):
	"""Pokemon Commands"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot       

	@commands.command(name="types")
	async def type_advantage(self, ctx):
		"""Pokemon type advantages."""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/info/weakness.jpg"))
  
def setup(bot: commands.Bot):
	bot.add_cog(Pokemon(bot))