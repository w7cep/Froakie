import asyncio
import random
from typing import Optional

import config
import nextcord
from aiohttp import request
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import BadArgument
import config

class PkmAutomation(commands.Cog, name="PkmAutomation"):
	"""Pokemon Automation Info Commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.command(name="arduino_release")
	@commands.guild_only()
	async def arduino_release(self, ctx):
		await ctx.send("https://github.com/PokemonAutomation/SwSh-Arduino/releases")
	
	@commands.command(name="arduino_wiki")
	@commands.guild_only()
	async def arduino_wiki(self, ctx):
		await ctx.send("https://github.com/PokemonAutomation/SwSh-Arduino/wiki")
 
	@commands.command(name="forkbot_release")
	@commands.guild_only()
	async def forkbot_release(self, ctx):
		await ctx.send("https://dev.azure.com/koigithub3088/SysBot_KoiFork/_build?definitionId=2&_a=summary")
	
	@commands.command(name="forkbot_wiki")
	@commands.guild_only()
	async def forkbot_wiki(self, ctx):
		await ctx.send("https://github.com/Koi-3088/ForkBot.NET/wiki")

	@commands.command(name="arduino_beta")
	@commands.guild_only()
	async def arduino_beta(self, ctx):
		await ctx.channel.trigger_typing()
		await ctx.send("https://discord.com/channels/829558837609889804/878558197475061760/897619516287242270")
  
def setup(bot: commands.Bot):
	bot.add_cog(PkmAutomation(bot))



	 
	
