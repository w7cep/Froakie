import nextcord
import random
from typing import Optional
from aiohttp import request
from nextcord.ext import commands
from nextcord import Member, Embed
from nextcord.ext.commands import BadArgument
class Random(commands.Cog, name="Random"):
	"""Random Commands"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command()
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
			await ctx.send(f"Rolls: {rolls}\nSum: {total}")
		except ValueError:
			await ctx.send("Dice must be in the format \_d\_ (example: 2d6)")

	@commands.command()
	async def choose(self, ctx: commands.Context, *args):
		"""Chooses a random item from a list
		
		Example: ?choose "First Option" "Second Option" "Third Option"
		"""
		try:
			choice = random.choice(args)
			await ctx.send(choice)
		except IndexError:
			await ctx.send("You must specify at least one argument.")
			
	@commands.command(name="joke")
	async def joke(self, ctx):
		selectjoke = random.choice([
			"Why don’t crabs give to charity? Because they’re shellfish.",
			"Why did the man name his dogs Rolex and Timex? Because they were watch dogs.",
			"My kid wants to invent a pencil with an eraser on each end, but I just don’t see the point."
		])
		await ctx.send(selectjoke)

	@commands.command(name="coinflip")
	async def coinflip(self, ctx):
		await ctx.send("Heads" if random.randint(1, 2) == 1 else "Tails")

	@commands.command(name="mirror")
	async def mirror(self, ctx, message):
		await ctx.send(message)

	@commands.command(name="length")
	async def length(self, ctx, sent):
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
		await ctx.send(f"World count : {word}, letter count : {letter}")

	@commands.command(name="fact")
	async def animal_fact(self, ctx, animal: str):
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
					await ctx.send(embed=embed)
					await ctx.message.delete()

				else:
					await ctx.send(f"API returned a {response.status} status.")

		else:
			await ctx.send("No facts are available for that animal.")   
	 
	@commands.command(
		 name="slap", 
		aliases=["hit"])
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
		await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")
		await ctx.message.delete()

	@slap_member.error
	async def slap_member_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.send("I can't find that member.")                          
  
def setup(bot: commands.Bot):
	bot.add_cog(Random(bot))