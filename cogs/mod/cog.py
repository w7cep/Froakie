import random
from typing import Optional
import nextcord, datetime
import nextcord.errors
from nextcord.ext import commands
from datetime import time
from nextcord.ext.commands import MissingPermissions
import asyncio
from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional
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
	await user.add_roles(role) # adds already existing muted role
	await ctx.send(f"{user.mention} has been muted for {reason}")

class Mod(commands.Cog, name="Mod"):
	"""Moderation commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

		self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

	async def __error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
				await ctx.send(error)
	"""//TODO Refine Ban, Unban, softban, Kick commands"""		
	@commands.command(aliases=["banish"])
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: Sinner=None, reason=None):
		"""Casts users out of heaven."""
		
		if not user: # checks if there is a user
			return await ctx.send("You must specify a user")
		
		try: # Tries to ban user
			await ctx.guild.ban(user)
			await ctx.send(f"{user.mention} was cast out of heaven for {reason}.")
		except nextcord.Forbidden:
			return await ctx.send("Are you trying to ban someone higher than the bot")

	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def softban(self, ctx, user: Sinner=None, reason=None):
		"""Temporarily restricts access to heaven."""
		
		if not user: # checks if there is a user
			return await ctx.send("You must specify a user")
		
		try: # Tries to soft-ban user
			await ctx.guild.ban(user)
			await ctx.send(f"Temporarily banned.\n"
		  					f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
			await ctx.guild.unban(user)
		except nextcord.Forbidden:
			return await ctx.send("Are you trying to soft-ban someone higher than the bot?")
	
	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def unban(self, ctx, id: int):
		user = await self.client.fetch_user(id)
		await ctx.guild.unban(user)

		unban= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		#unban.add_field(name='User Affected:', value=f'`{member.name}`', inline=True)
		#unban.add_field(name='User ID:', value=f'`{member.id}`', inline=True)
		unban.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		unban.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		unban.add_field(name='Action Performed:', value='`UnBan`', inline=True)
		unban.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon_url)
		#unban.set_thumbnail(url=member.avatar_url)
		unban.timestamp = datetime.datetime.utcnow()

		await ctx.send(embed=unban)

	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def kick(self, ctx, user: Sinner=None, reason=None):
		if not user: # checks if there is a user 
			return await ctx.send("You must specify a user")
		
		try: # tries to kick user
			await ctx.guild.kick(user)
			await ctx.send(f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
		except nextcord.Forbidden:
			return await ctx.send("Are you trying to kick someone higher than the bot?")

	'''@commands.command()
	async def purge(self, ctx, limit: int):
		"""Bulk deletes messages"""
		
		await ctx.purge(limit=limit + 1) # also deletes your own message
		await ctx.send(f"Bulk deleted `{limit}` messages")''' 
	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def mute(self, ctx, user: Sinner, reason=None):
		"""Gives them hell."""
		await mute(ctx, user, reason or "treason") # uses the mute function
		
	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def unmute(self, ctx, user: Redeemed):
		"""Unmutes a muted user"""
		await user.remove_roles(nextcord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
		await ctx.send(f"{user.mention} has been unmuted")
		"""//TODO: Fix Block and Unblock command. """
	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def block(self, ctx, user: Sinner=None):
		"""
		Blocks a user from chatting in current channel.
		   
		Similar to mute but instead of restricting access
		to all channels it restricts in current channel.
		"""
								
		if not user: # checks if there is user
			return await ctx.send("You must specify a user")
								
		await self.set_permissions(user, send_messages=False) # sets permissions for current channel
	
	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def unblock(self, ctx, user: Sinner=None):
		"""Unblocks a user from current channel"""
								
		if not user: # checks if there is user
			return await ctx.send("You must specify a user")
		
		await self.set_permissions(user, send_messages=True) # gives back send messages permissions
								

	@commands.command(name="addprofanity", aliases=["addswears", "addcurses"])
	@commands.has_permissions(administrator=True)
	async def add_profanity(self, ctx, *words):
		'''Add cuss word to file.'''
		with open("./data/profanity.txt", "a", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in words]))

		profanity.load_censor_words_from_file("./data/profanity.txt")
		await ctx.send("Action complete.")

	@commands.command(name="delprofanity", aliases=["delswears", "delcurses"])
	@commands.has_permissions(administrator=True)
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
"""
	@commands.command(name="echo")
	@commands.has_permissions(administrator=True)
	async def echo(self, ctx):
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

	@commands.command(name="mute")
	@commands.has_permissions(administrator=True) #permissions
	async def mute(self, ctx, user : nextcord.Member):
		role = nextcord.utils.get(user.guild.roles, name="muted")
		if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
			return await ctx.send('**:x: | That role is above your top role!**')
		else:
			await user.add_roles(role) #adds role if not already has it
			await ctx.send(f"{user.mention} has been {role}")

	@commands.command(name="unmute")
	@commands.has_permissions(administrator=True) #permissions
	async def unmute(self, ctx, user : nextcord.Member):
		role = nextcord.utils.get(user.guild.roles, name="muted")
		if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
			return await ctx.send('**:x: | That role is above your top role!**')
		else:
			await user.remove_roles(role) #removes the role if user already has
			await ctx.send(f"{user.mention} has been un{role}")
"""

def setup(bot: commands.Bot):
	bot.add_cog(Mod(bot))
	