import nextcord
from nextcord.ext import commands

class CustomCommands(commands.Cog, name="Custom_Commands"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="server_invite") 
	async def server_invite(self, ctx):
		"""A useful command that displays a permanent invite link."""
		embed = nextcord.Embed(
			title="__Permanent Invite Link__",
			description="https://discord.gg/dm7gSAT68d",
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(CustomCommands(bot))
