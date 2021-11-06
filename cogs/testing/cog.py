from typing import List
import nextcord
from nextcord import Embed
from nextcord.ext import commands
import asyncio
import pokebase as pb
from aiohttp import request

class RandD(commands.Cog, name="R&D"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="say")
	@commands.is_owner()
	async def say(self, ctx, channel:nextcord.TextChannel, *, message):
		"""Make the bot say something in the specified channel."""
		if channel is not None:
			await ctx.channel.trigger_typing()
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
			embed.set_author(name=f"Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
		await ctx.channel.trigger_typing()
		await channel.send(embed=embed)

	@commands.command(name="echo")
	@commands.has_role(829942684947841024)
	async def echo(self, ctx):
		"""Have the bot echo something and hide the evidence."""
		await ctx.message.delete()
		embed = nextcord.Embed(
			title="Please tell me what you want me to repeat!",
			description="This request will timeout after 1 minute.",
		)
		await ctx.channel.trigger_typing()
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
				await ctx.channel.trigger_typing()
				await ctx.send(msg.content)
		except asyncio.TimeoutError:
			await sent.delete()
			await ctx.channel.trigger_typing()
			await ctx.send("Cancelling", delete_after=10)

	@commands.command(name="berry")
	@commands.guild_only()
	async def berry(self, ctx, Name=None):
		if Name is None:
			await ctx.send("please specify a berry name")
		else:
			berry = pb.APIResource('berry', f'{Name}')
			await ctx.send(f"Name:{berry.name}\nNatural Gift Type:{berry.flavor.name}")

	@commands.command(name="pkm")
	async def pkm(self, ctx, pokemon: str):
		"""Gives you a fact for these animals: "dog", "cat", "panda", "fox", "bird", "koala"."""
		if pokemon != None:
			fact_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
			image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon}"

			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]

				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					embed = Embed(title=f"{pokemon.title()} fact",
								  description=data,
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
			await ctx.send("No facts are available for that pokemon.")   

def setup(bot: commands.Bot):
	bot.add_cog(RandD(bot))
