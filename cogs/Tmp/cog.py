import nextcord
from nextcord.ext import commands

class CustomCommands(commands.Cog, name="Custom_Commands"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot



def setup(bot: commands.Bot):
	bot.add_cog(CustomCommands(bot))
