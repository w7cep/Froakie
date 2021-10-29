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
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.command(name="raid_request")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def raid_request(self, ctx, reason = None):
     
		suggestion_channel = await ctx.guild.fetch_channel(config.SUGGESTION_CHANNEL_ID)
  
		if ctx.channel.id == 875571213844488223:   
			user = ctx.author
			supem = nextcord.Embed(title=f"{user} requested.", description=f"{reason}", color=0x00ff00)
			supem.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
			supem.set_image(url="https://cdn.discordapp.com/attachments/901687898452131860/902400527621566504/greninja_banner.jpg")
			supem.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
			supem.set_author(name=f"Greninja Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
			supem.add_field(name=f"Thanks for the suggestion!", value="Staff will get to your suggestion soon...")
			await suggestion_channel.send(embed=supem)
   
		elif ctx.channel.id != 875571213844488223:
			await ctx.send("❌ You can't use this command here!")

	@commands.command()
	@commands.has_role(829942684947841024) 
	async def temp_mute(ctx, user: nextcord.Member=None, mute_time: int = None, reason = None):
		if reason == None:
			reason = "no reason"
		if not user:
			await ctx.send("Who do you want me to mute?")
			return
		role = nextcord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't 
		await user.add_roles(role) # adds already existing muted role
		await ctx.send(f"{user.mention} has been muted for {reason}")

		await asyncio.sleep(mute_time)
		await user.remove_roles(role)
		await ctx.send("ok times up")
 
def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))



	 
	
