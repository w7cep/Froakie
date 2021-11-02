from typing import List
import nextcord
from nextcord.ext import commands
import config

class Testing(commands.Cog, name="Testing"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="request")
	async def request(self, ctx, *, reason = None):
		bot = self.bot.user
		user = ctx.author
		channel = await ctx.guild.fetch_channel(config.SUGGESTION_CHANNEL_ID)
		if reason is None:
			await ctx.send("Please suggest a 'Den' or 'Max Lair Path'.")
		else:
			embed = nextcord.Embed(title=f"{user} requested support.", description= "An admin will be with you shortly...", color=0x00ff00)
			embed.add_field(name="Suggestion", value=f"{reason}")
			embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
			embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
			embed.set_footer(text=f"{user.name}{user.discriminator}--ID:{user.id}", icon_url=user.avatar.url)
			embed.set_author(name=bot.name, icon_url=bot.avatar.url)
			await ctx.channel.trigger_typing()
			await channel.send(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))
