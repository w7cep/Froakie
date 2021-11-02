import platform
import random
from typing import Optional

import config
import nextcord
from aiohttp import request
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import BadArgument


class Misc(commands.Cog, name="Misc"):
	"""Misc. Commands"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def info(self, ctx):
		await ctx.send("Invalid sub-command specified")

	@info.command(name="stats") 
	async def stats(self, ctx):
		"""A useful command that displays bot statistics."""
		pythonVersion = platform.python_version()
		dpyVersion = nextcord.__version__
		serverCount = len(self.bot.guilds)
		memberCount = len(set(self.bot.get_all_members()))
		version = "v1.1.0"
		developer = "<@741118153299591240>"
		embed = nextcord.Embed(
			title=f"{self.bot.user.name} Stats",
			description="Useful stats.",
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)
		embed.add_field(name="Bot Version:", value=version)
		embed.add_field(name="Python Version:", value=pythonVersion)
		embed.add_field(name="nextcord Version", value=dpyVersion)
		embed.add_field(name="Total Guilds:", value=serverCount)
		embed.add_field(name="Total Users:", value=memberCount)
		embed.add_field(name="Bot Developers:", value=developer)

		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)

	@info.command(name="wiki")
	@commands.guild_only()
	async def wiki(self, ctx, msg):
		"""Get info from wikipedia."""
		url: str = f"https://wikipedia.org/wiki/{msg}"
		await ctx.channel.trigger_typing()
		await ctx.send(f"Here : {url}")

	@info.command(name="emoji")
	@commands.has_role(829942684947841024)
	async def emoji(self, ctx, emoji: nextcord.Emoji = None):
		"""Display information about an emoji in the server."""
		if not emoji:
					await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

		try:
					emoji = await emoji.guild.fetch_emoji(emoji.id)
		except nextcord.NotFound:
					await ctx.channel.trigger_typing()
					await ctx.send("I could not find this emoji in the given guild.")

		is_managed = "Yes" if emoji.managed else "No"
		is_animated = "Yes" if emoji.animated else "No"
		requires_colons = "Yes" if emoji.require_colons else "No"
		creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
		can_use_emoji = (
			"Everyone"
			if not emoji.roles
			else " ".join(role.name for role in emoji.roles)
		)

		description = f"""
		**General:**
		**- Name:** {emoji.name}
		**- Id:** {emoji.id}
		**- URL:** [Link To Emoji]({emoji.url})
		**- Author:** {emoji.user.name}
		**- Time Created:** {creation_time}
		**- Usable by:** {can_use_emoji}
		
		**Other:**
		**- Animated:** {is_animated}
		**- Managed:** {is_managed}
		**- Requires Colons:** {requires_colons}
		**- Guild Name:** {emoji.guild.name}
		**- Guild Id:** {emoji.guild.id}
		"""

		embed = nextcord.Embed(
		title=f"**Emoji Information for:** `{emoji.name}`",
		description=description,
		colour=0xADD8E6,
		)
		embed.set_thumbnail(url=emoji.url)
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)

	@commands.command(name="ping")
	async def ping(self, ctx: commands.Context):
		"""Checks for a response from the bot"""
		await ctx.channel.trigger_typing()
		await ctx.send(f"Pong! (Latency: {round(self.bot.latency * 1000)}ms)")

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def random(self, ctx):
		await ctx.send("Invalid sub-command specified")

	@random.command()
	async def roll(self, ctx: commands.Context, dice: str):
		"""Rolls a given amount of dice in the form _d_
		
		Example: ?roll 2d20
		"""
		try:
			rolls = ""
			total = 0
			amount, die = dice.split("d")
			for _ in range(int(amount)):
				roll = random.randint(1, int(die))
				total += roll
				rolls += f"{roll} "
			await ctx.channel.trigger_typing()
			await ctx.send(f"Rolls: {rolls}\nSum: {total}")
		except ValueError:
			await ctx.channel.trigger_typing()
			await ctx.send("Dice must be in the format \_d\_ (example: 2d6)")

	@random.command()
	async def choose(self, ctx: commands.Context, *args):
		"""Chooses a random item from a list
		
		Example: ?choose "First Option" "Second Option" "Third Option"
		"""
		try:
			choice = random.choice(args)
			await ctx.channel.trigger_typing()
			await ctx.send(choice)
		except IndexError:
			await ctx.channel.trigger_typing()
			await ctx.send("You must specify at least one argument.")
			
	@random.command(name="joke")
	async def joke(self, ctx):
		"""Random dad joke."""
		selectjoke = random.choice([
			"Why don’t crabs give to charity? Because they’re shellfish.",
			"Why did the man name his dogs Rolex and Timex? Because they were watch dogs.",
			"My kid wants to invent a pencil with an eraser on each end, but I just don’t see the point."
		])
		await ctx.channel.trigger_typing()
		await ctx.send(selectjoke)

	@random.command(name="coinflip")
	async def coinflip(self, ctx):
		"""Flip a coin."""
		await ctx.channel.trigger_typing()
		await ctx.send("Heads" if random.randint(1, 2) == 1 else "Tails")

	@random.command(name="mirror")
	async def mirror(self, ctx, message):
		"""Bot will mirror your message."""
		await ctx.channel.trigger_typing()
		await ctx.send(message)

	@random.command(name="length")
	async def length(self, ctx, sent):
		"""Gives you the details of a sentence."""
		sentence: str = ctx.message.content[7:]
		print(sentence)
		length: int = len(sentence)
		i = 0
		count: int = 0
		while i < length - 1:
			i += 1
			if sentence[i] == " ":
				count += 1
		word = count + 1
		letter = i + 1
		await ctx.channel.trigger_typing()
		await ctx.send(f"World count : {word}, letter count : {letter}")

	@random.command(name="fact")
	async def animal_fact(self, ctx, animal: str):
		"""Gives you a fact for these animals: "dog", "cat", "panda", "fox", "bird", "koala"."""
		if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala", ):
			fact_url = f"https://some-random-api.ml/facts/{animal}"
			image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]

				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					embed = Embed(title=f"{animal.title()} fact",
								  description=data["fact"],
								  colour=ctx.author.colour)
					if image_link is not None:
						embed.set_image(url=image_link)
					await ctx.channel.trigger_typing()
					await ctx.send(embed=embed)
					await ctx.message.delete()

				else:
					await ctx.channel.trigger_typing()
					await ctx.send(f"API returned a {response.status} status.")

		else:
			await ctx.channel.trigger_typing()
			await ctx.send("No facts are available for that animal.")   
	 
	@random.command(
		 name="slap", 
		aliases=["hit"])
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
		"""Slap another member for a reason or no reason."""
		await ctx.channel.trigger_typing()
		await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")
		await ctx.message.delete()

	@slap_member.error
	async def slap_member_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.channel.trigger_typing()
			await ctx.send("I can't find that member.")

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def reaction(self, ctx):
		await ctx.send("Invalid sub-command specified")

	@reaction.command(name="tableflip")
	async def tableflip(self, ctx):
		# I hope this unicode doesn't break
		"""(╯°□°）╯︵ ┻━┻"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/tableflip.gif"))

	@reaction.command(name="unflip")
	async def unflip(self, ctx):
		# I hope this unicode doesn't break
		"""┬─┬﻿ ノ( ゜-゜ノ)"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/unflip.gif"))

	@reaction.command(name="triggered")
	async def triggered(self, ctx):
		"""*TRIGGERED*"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/triggered.gif"))

	@reaction.command(name="delet")
	async def delet(self, ctx):
		"""Delet this"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/delet_this.png"))

	@reaction.command(name="weirdshit")
	async def weirdshit(self, ctx):
		"""WHY ARE YOU POSTING WEIRD SHIT?!?!?!"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/weirdshit.jpg"))

	@reaction.command(name="filth")
	async def filth(self, ctx):
		"""THIS IS ABSOLUTELY FILTHY!"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/filth.gif"))

	@reaction.command(name="heckoff")
	async def heckoff(self, ctx):
		"""heck off fools"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/heckoff.png"))

	@reaction.command(name="repost")
	async def repost(self, ctx):
		"""It's just a repost smh"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/repost.gif"))

	@reaction.command(name="boi")
	async def boi(self, ctx):
		"""BOI"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/reactions/boi.jpg"))

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def pokemon(self, ctx):
		await ctx.send("Invalid sub-command specified")
  
	@pokemon.command(name="types")
	async def type_advantage(self, ctx):
		"""Pokemon type advantages."""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/info/weakness.jpg"))

	@pokemon.command(name="request")
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
	bot.add_cog(Misc(bot))
