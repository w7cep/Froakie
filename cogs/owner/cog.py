import nextcord
from nextcord.ext import commands

class Owner(commands.Cog, name="Owner"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	@commands.has_role(881434748222857216)
	async def toggle(self, ctx, *, command):
		"""Toggle commands on or off."""
		command = self.bot.get_command(command)
		if command == None:
			await ctx.send("couldn't find that command ._.")
		elif ctx.command == command:
			await ctx.send('you can not disable this command._.')
		else:
			command.enabled = not command.enabled
			ternary = "enabled" if command.enabled else "disabled"
			await ctx.send(f'command {command.qualified_name} has been {ternary}')

def setup(bot: commands.Bot):
	bot.add_cog(Owner(bot))
