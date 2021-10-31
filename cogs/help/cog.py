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

	@commands.command(name="support")
	async def support(self, ctx, *, reason = None):
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
		await ctx.channel.trigger_typing()
		await channel.send(f"{user.mention}")
		embed = nextcord.Embed(title=f"{user} requested support.", description= "Either an admin or support staff will be with you shortly...", color=0x00ff00)
		embed.add_field(name="Reason", value=f"``{reason}``")
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.channel.trigger_typing()
		await channel.send(embed=embed)

# setup functions for bot
def setup(bot: commands.Bot):
	bot.add_cog(HelpCog(bot))