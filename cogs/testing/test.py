import random
from typing import Optional

import nextcord
from aiohttp import request
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import BadArgument

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
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.command(name="block", hidden=True)
	@commands.has_role(829942684947841024) 
	async def block(self, ctx, user: Sinner=None, channel: nextcord.Channel = None):
					
		if not user: # checks if there is user
			return await ctx.send("You must specify a user")
		if channel == None:
			channel = ctx.channel
   
		await channel.set_permissions(user, send_messages=False, view_channel=True, read_message_history=True) # sets permissions for current channel
		await channel.send(f"🚫{user.mention} has been blocked in {channel.mention} 🚫")
	
	@commands.command(name="unblock", hidden=True)
	@commands.has_role(829942684947841024) 
	async def unblock(self, ctx, user: Sinner=None, channel: nextcord.Channel = None):
					
		if not user: # checks if there is user
			return await ctx.send("You must specify a user")
		if channel == None:
			channel = ctx.channel
   
		await channel.set_permissions(user, send_messages=None, view_channel=None, read_message_history=None) # sets permissions for current channel
		await channel.send(f"✅{user.mention} has been unblocked in {channel.mention}✅")
	 
def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))
