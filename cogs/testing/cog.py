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

class Sinner(commands.Converter):
	async def convert(self, ctx, argument):
		argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
		permission = argument.guild_permissions.manage_messages # can change into any permission
		if not permission: # checks if user has the permission
			return argument # returns user object
		else:
			raise commands.BadArgument("You cannot punish other staff members") # t

class Testing(commands.Cog, name="Testing"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot, *args, **kwargs):
		super().__init__(bot, *args, **kwargs)
		self.bot = bot

		# create the background task and run it in the background
		self.bg_task = self.loop.create_task(self.my_background_task())


	async def my_background_task(self):
		await self.wait_until_ready()
		counter = 0
		channel = self.get_channel(891852099653083186) # channel ID goes here
		while not self.is_closed():
			counter += 1
			await channel.send(counter)
			await asyncio.sleep(60) # task runs every 60 seconds

def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))
