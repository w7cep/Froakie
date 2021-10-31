import random
from typing import Optional
import nextcord, datetime
import nextcord.errors
from datetime import time
from nextcord.ext.commands import MissingPermissions
import asyncio
from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from better_profanity import profanity
from nextcord import Embed, Member, NotFound, Object
from nextcord.utils import find
from nextcord.ext.commands import Cog, Greedy, Converter
from nextcord.ext.commands import CheckFailure, BadArgument
from nextcord.ext.commands import command, has_permissions, bot_has_permissions
from nextcord.ext import commands
from db import db
import requests
import json

profanity.load_censor_words_from_file("./data/profanity.txt")

# This prevents staff members from being punished 
class Sinner(commands.Converter):
	async def convert(self, ctx, argument):
		argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
		permission = argument.guild_permissions.manage_messages # can change into any permission
		if not permission: # checks if user has the permission
			return argument # returns user object
		else:
			raise commands.BadArgument("You cannot punish other staff members") # tells user that target is a staff member

# Checks if you have a muted role
class Redeemed(commands.Converter):
	async def convert(self, ctx, argument):
		argument = await commands.MemberConverter().convert(ctx, argument) # gets member object
		muted = nextcord.utils.get(ctx.guild.roles, name="Muted") # gets role object
		if muted in argument.roles: # checks if user has muted role
			return argument # returns member object if there is muted role
		else:
			raise commands.BadArgument("The user was not muted.") # self-explainatory
			
# Checks if there is a muted role on the server and creates one if there isn't
async def mute(ctx, user, reason):
	role = nextcord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't 
	await user.add_roles(role)
	await ctx.channel.trigger_typing()# adds already existing muted role
	await ctx.send(f"{user.mention} has been muted for {reason}")

class MemberMod(commands.Cog, name="Member Mod"):
	"""Moderation commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

		self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

	async def __error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
				await ctx.send(error)
	
	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def member(self, ctx):
		await ctx.send("Invalid sub-command specified")
 
	@member.command(name="ban")
	@commands.has_role(829942684947841024)
	async def ban(self, ctx, id: int):
		"""Ban a user from the server."""
		user = await self.bot.fetch_user(id)
		await ctx.guild.ban(user)

		ban= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		ban.add_field(name='User Affected:', value=f'`{user.name}{user.discriminator}`', inline=True)
		ban.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		ban.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		ban.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		ban.add_field(name='Action Performed:', value='`Ban`', inline=True)
		ban.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		ban.set_thumbnail(url=user.avatar.url)
		ban.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		ban.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=ban)

	@member.command(name="softban")
	@commands.has_role(829942684947841024) 
	async def softban(self, ctx, id: int):
		"""Softban a user from the server."""
		user = await self.bot.fetch_user(id)

		softban= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		softban.add_field(name='User Affected:', value=f'`{user.name}{user.discriminator}`', inline=True)
		softban.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		softban.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		softban.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		softban.add_field(name='Action Performed:', value='`Softban`', inline=True)
		softban.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		softban.set_thumbnail(url=user.avatar.url)
		softban.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		softban.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		await ctx.guild.ban(user)
		await ctx.guild.unban(user)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=softban)
	
	@member.command(name="unban")
	@commands.has_role(829942684947841024)
	async def unban(self, ctx, id: int):
		"""Unban a user from the server."""
		user = await self.bot.fetch_user(id)
		await ctx.guild.unban(user)

		unban= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		unban.add_field(name='User Affected:', value=f'`{user.name}{user.discriminator}`', inline=True)
		unban.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		unban.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=False)
		unban.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		unban.add_field(name='Action Performed:', value='`Unban`', inline=True)
		unban.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		unban.set_thumbnail(url=user.avatar.url)
		unban.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		unban.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=unban)

	@member.command(name="kick")
	@commands.has_role(829942684947841024)
	async def kick(self, ctx, id: int):
		"""Kick a user from the server."""
		user = await self.bot.fetch_user(id)
		await ctx.guild.kick(user)

		kick= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		kick.add_field(name='User Affected:', value=f'`{user.name}{user.discriminator}`', inline=True)
		kick.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		kick.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		kick.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		kick.add_field(name='Action Performed:', value='`Kick`', inline=True)
		kick.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		kick.set_thumbnail(url=user.avatar.url)
		kick.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		kick.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=kick)
 
	@member.command(name="mute")
	@commands.has_role(829942684947841024) 
	async def mute(self, ctx, user: Sinner, reason=None):
		"""Gives them hell."""
		await mute(ctx, user, reason or "being sus") # uses the mute function
		
	@member.command(name="unmute")
	@commands.has_role(829942684947841024)
	async def unmute(self, ctx, user: Redeemed):
		"""Unmutes a muted user"""
		await user.remove_roles(nextcord.utils.get(ctx.guild.roles, name="Muted"))
		await ctx.channel.trigger_typing()# removes muted role
		await ctx.send(f"{user.mention} has been unmuted")
  
	# TODO Make: temp_mute command
	
	@member.command(name="block")
	@commands.has_role(829942684947841024) 
	async def block(self, ctx, user: Sinner=None, channel: nextcord.TextChannel = None, reason = None):
					
		if not user: # checks if there is user
			return await ctx.send("You must specify a user")
		if channel == None:
			channel = ctx.channel
		if reason == None:
			reason = "no reason"
		await channel.set_permissions(user, send_messages=False, view_channel=True, read_message_history=True)# sets permissions for current channel
		await ctx.channel.trigger_typing()
		await channel.send(f"🚫{user.mention} has been blocked in {channel.mention} 🚫 for {reason}")
	
	@member.command(name="unblock")
	@commands.has_role(829942684947841024) 
	async def unblock(self, ctx, user: Sinner=None, channel: nextcord.TextChannel = None, reason = None):
					
		if not user: # checks if there is user
			return await ctx.send("You must specify a user")
		if channel == None:
			channel = ctx.channel
   
		await channel.set_permissions(user, send_messages=None, view_channel=None, read_message_history=None) # sets permissions for current channel
		await ctx.channel.trigger_typing()
		await channel.send(f"✅{user.mention} has been unblocked in {channel.mention}✅")

	@member.command(name="addrole")
	@commands.is_owner() #permissions
	async def give_role(self, ctx, user : nextcord.Member, *, role : nextcord.Role):
		"""Give role to member."""
		if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
			return await ctx.send('**:x: | That role is above your top role!**')
		if role in user.roles:
			await user.remove_roles(role) #removes the role if user already has
			await ctx.send(f"Removed {role} from {user.mention}") 
		else:
			await user.add_roles(role) #adds role if not already has it
		await ctx.channel.trigger_typing()
		await ctx.send(f"Added {role} to {user.mention}")
			
	@give_role.error
	async def role_error(self, ctx, error):
		if isinstance(error, MissingPermissions):
			await ctx.channel.trigger_typing()
			await ctx.send('**:x: | You do not have permission to use this command!**')

	@member.command(name="info") 
	@commands.has_role(829942684947841024)
	@commands.guild_only()
	async def memberinfo(self, ctx, *, user : nextcord.Member = None):
		
		"""
		Get information about you, or a specified user.
		`$$ui <user>`
		`user`: The user who you want information about. Can be an ID, mention or name.
		"""
		if user is None:
			user = ctx.author
			
		embed = nextcord.Embed(title=f"{user.name}'s Stats and Information.")
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text="ID: {user.id}")
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		embed.add_field(name="__**ID:**__", value=f"{user.id}")
		embed.add_field(name="__**General information:**__", value=f"**Discord Name:** {user}\n"
																   f"**Account created:** {user.created_at.__format__('%A %d %B %Y at %H:%M')}", inline=False)        
		embed.add_field(name="__**Server-related information:**__", value=f"**Nickname:** {user.nick}\n"
																		  f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
																		  f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}")
		await ctx.channel.trigger_typing()
		return await ctx.send(embed=embed)


def setup(bot: commands.Bot):
	bot.add_cog(MemberMod(bot))
	