import random
from typing import Optional

import nextcord
from aiohttp import request
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import BadArgument


class Testing(commands.Cog, name="Testing"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
'''	@commands.command(name="block")
	async def block(self, ctx, *, user : nextcord.Member = None, reason = None):
		
		if not user: # checks if there is user
			return await ctx.send("You must specify a user")

		"""amount2 = 1
		await ctx.channel.purge(limit=amount2)"""
		channel = ctx.channel
		await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
		perms = channel.overwrites_for(user)
		await channel.set_permissions(user, view_channel=not perms.view_channel)
		await channel.set_permissions(user, read_message_history=not perms.read_message_history)
		await channel.set_permissions(user, send_messages=not perms.send_messages)
		await channel.send(f"🚫{user.mention} has been blocked 🚫")
		supem = nextcord.Embed(title=f"{user} requested support.", description= "", color=0x00ff00)
		supem.add_field(name="Reason", value=f"``{reason}``")
		supem.set_footer(text=f"Either an admin or support staff will be with you shortly...")
		await channel.send(embed=supem)'''
	 
	 
def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))
