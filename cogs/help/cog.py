import nextcord
from nextcord.ext import commands
from .help_command import NewHelpCommand


class HelpCog(commands.Cog, name="Help"):
	"""Displays help information for commands and cogs"""

	def __init__(self, bot: commands.Bot):
		self.__bot = bot
		self.__original_help_command = bot.help_command
		bot.help_command = NewHelpCommand()
		bot.help_command.cog = self

	def cog_unload(self):
		self.__bot.help_command = self.__original_help_command

	@commands.command(name="tech_support")
	async def tech_support(self, ctx, *, reason = None):
		guild = ctx.guild
		user = ctx.author
		amount2 = 1
		await ctx.channel.purge(limit=amount2)
		channel = await guild.create_text_channel(f'Ticket {user}')
		await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
		perms = channel.overwrites_for(user)
		await channel.set_permissions(user, view_channel=not perms.view_channel)
		await channel.set_permissions(user, read_message_history=not perms.read_message_history)
		await channel.set_permissions(user, send_messages=not perms.send_messages)
		await channel.send(f"{user.mention}")
		supem = nextcord.Embed(title=f"{user} requested support.", description= "", color=0x00ff00)
		supem.add_field(name="Reason", value=f"``{reason}``")
		supem.set_footer(text=f"Either an admin or support staff will be with you shortly...")
		await channel.send(embed=supem)

# setup functions for bot
def setup(bot: commands.Bot):
	bot.add_cog(HelpCog(bot))