from random import choice
from typing import Optional
import asyncio
import platform
import nextcord, datetime
from nextcord import Member
from nextcord.ext.commands import BadArgument
from nextcord.ext.commands import command
from nextcord.ext import commands
from better_profanity import profanity

profanity.load_censor_words_from_file("./data/profanity.txt")
class ServerMod(commands.Cog, name="ServerMod"):
	"""Greeting commands"""
	
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self._last_member = None
		
	@commands.command(name="addswears", aliases=["addprofanity", "addcurses"])
	@commands.has_role(829942684947841024)
	async def add_profanity(self, ctx, *words):
		'''Add cuss word to file.'''
		with open("./data/profanity.txt", "a", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in words]))

		profanity.load_censor_words_from_file("./data/profanity.txt")
		await ctx.send("Action complete.")

	@commands.command(name="delswears", aliases=["delprofanity", "delcurses"])
	@commands.has_role(829942684947841024)
	async def remove_profanity(self, ctx, *words):
		'''Delete cuss word from file.'''
		with open("./data/profanity.txt", "r", encoding="utf-8") as f:
			stored = [w.strip() for w in f.readlines()]

		with open("./data/profanity.txt", "w", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in stored if w not in words]))

		profanity.load_censor_words_from_file("./data/profanity.txt")
		await ctx.send("Action complete.")

	@commands.Cog.listener()
	async def on_message(self, message):
		def _check(m):
			return (m.author == message.author
					and len(m.mentions)
					and (datetime.utcnow()-m.created_at).seconds < 60)

		if profanity.contains_profanity(message.content):
			await message.delete()
			await message.channel.send("You can't use that word here.", delete_after=10)

	@commands.command(name="say")
	@commands.is_owner()
	async def say(self, ctx, channel:nextcord.TextChannel, *, message):
		"""Make the bot say something in the specified channel."""
		if channel is not None:
			await channel.send(message)

	@commands.command(name="say_embed")
	@commands.is_owner()
	async def say_embed(self, ctx, channel:nextcord.TextChannel, *, message):
		"""Make the bot say something in the specified channel as an embed."""
		if channel is not None:
			embed= nextcord.Embed(description=f"{message}")
			embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
			embed.set_image(url="https://cdn.discordapp.com/attachments/901687898452131860/902400527621566504/greninja_banner.jpg")
			embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
			embed.set_author(name=f"Greninja Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
		await channel.send(embed=embed)

	"""//TODO-Use the echo command as a base to make a tempmute command."""
	@commands.command(name="echo")
	@commands.has_role(829942684947841024)
	async def echo(self, ctx):
		"""Have the bot echo something and hide the evidence."""
		await ctx.message.delete()
		embed = nextcord.Embed(
			title="Please tell me what you want me to repeat!",
			description="This request will timeout after 1 minute.",
		)
		sent = await ctx.send(embed=embed)

		try:
			msg = await self.bot.wait_for(
				"message",
				timeout=60,
				check=lambda message: message.author == ctx.author
				and message.channel == ctx.channel,
			)
			if msg:
				await sent.delete()
				await msg.delete()
				await ctx.send(msg.content)
		except asyncio.TimeoutError:
			await sent.delete()
			await ctx.send("Cancelling", delete_after=10)

def setup(bot: commands.Bot):
	bot.add_cog(ServerMod(bot))
