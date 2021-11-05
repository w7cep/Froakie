import nextcord
from nextcord.ext import commands
from .dropdown_view import DropdownView

class DropDown(commands.Cog, name="DropDown"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot
  
@commands.command(name="lang")
async def lang(self, ctx):
	view = DropdownView()
	await ctx.send('choose a language!')

def setup(bot: commands.Bot):
	bot.add_cog(DropDown(bot))