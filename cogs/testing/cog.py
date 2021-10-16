import nextcord
import random
from typing import Optional
from aiohttp import request
from nextcord.ext import commands
from nextcord import Member, Embed
from nextcord.ext.commands import BadArgument

class Testing(commands.Cog, name="Testing"):
	"""Returns random results"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="add", descripton="Adds two numbers together.")
	async def add(ctx, left: int, right: int):
			await ctx.send(left + right)

	@commands.command(
		 name="repeat",
		description="Repeat a message a number of times."
	)
	async def repeat(ctx, times: int, content='repeating...'):
			for i in range(times):
				await ctx.send(content)

	@commands.command(name="cmd")
	@commands.has_permissions(administrator=True)
	@commands.guild_only()
	async def cmd(self, ctx):

		"""Test Embed."""
		
		version = "v1.0.0"
		
		embed = nextcord.Embed(
			title="__**Server Commands**__",
			description="List of all server commands.",
			colour=nextcord.Colour.blue()
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_author(name="Greninja Mod", icon_url="https://cdn.discordapp.com/avatars/866572422438060052/cb32b40409c7df4d147c400582f939ac.webp?size=4096")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		###########################################################################################################################
		embed.add_field(name="__**Admin Commands:**__", value=f"**$$clean** : Cleans the chat of bot messages.\n"
												f"**$$role** : Give role to member.\n"
												f"**$$memberinfo, $$mi** : Get information about a member.\n"
												f"**$$addprofanity** : Add cuss word to file.\n" 
												f"**$$delprofanity** : Delete cuss word from file.\n"
												f"**$$cmd** : List all bot commands."
												f"**$$emojiinfo** : Get info about an emoji.\n"
												f"**$$channelstats, $$cs** : Get channel stats.\n" 
												f"**$$new category <role> <name>** : Create a new category.\n"
												f"**$$new channel <role> <name>** : Create a new channel.\n" 
												f"**$$delete category <role> <name>** : Create a new category.\n"
												f"**$$delete channel <role> <name>** : Create a new channel.\n" 
												f"**$$lockdown** : Lock or Unlock a channel.\n", inline=False)
		
		embed.add_field(name="__**General Commands:**__", value=f"**$$hello** : Say hello to the bot.\n"
												f"**$$bye** : Say bye to the bot.\n"
												f"**$$slap** : Slap another member.\n"
												f"**$$fact** : Get a fact about an animal.\n"
												f"**$$stats** : Get bot stats.", inline=False)                                                    
		embed.set_footer(text=f"Bot is running {version}")
		await ctx.send(embed=embed)
		

def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))