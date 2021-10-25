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
		
	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def ban(self, ctx, id: int):
		user = await self.bot.fetch_user(id)
		await ctx.guild.ban(user)

		ban= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		ban.add_field(name='User Affected:', value=f'`{user.name}``{user.discriminator}`', inline=True)
		ban.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		ban.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		ban.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		ban.add_field(name='Action Performed:', value='`Ban`', inline=True)
		ban.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		ban.set_thumbnail(url=user.avatar.url)
		#unban.timestamp = datetime.datetime.utcnow()

		await ctx.send(embed=ban)

	@commands.command()
	@commands.has_permissions(administrator=True) 
	async def softban(self, ctx, id: int):
		"""Temporarily restricts access to heaven."""
		user = await self.bot.fetch_user(id)

		softban= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		softban.add_field(name='User Affected:', value=f'`{user.name}``{user.discriminator}`', inline=True)
		softban.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		softban.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		softban.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		softban.add_field(name='Action Performed:', value='`Softban`', inline=True)
		softban.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		softban.set_thumbnail(url=user.avatar.url)
		#unban.timestamp = datetime.datetime.utcnow()
		await ctx.guild.ban(user)
		await ctx.guild.unban(user)
		await ctx.send(embed=softban)
	
	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def unban(self, ctx, id: int):
		user = await self.bot.fetch_user(id)
		await ctx.guild.unban(user)

		unban= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		unban.add_field(name='User Affected:', value=f'`{user.name}``{user.discriminator}`', inline=True)
		unban.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		unban.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		unban.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		unban.add_field(name='Action Performed:', value='`Unban`', inline=True)
		unban.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		unban.set_thumbnail(url=user.avatar.url)
		#unban.timestamp = datetime.datetime.utcnow()

		await ctx.send(embed=unban)

	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def kick(self, ctx, id: int):
		user = await self.bot.fetch_user(id)
		await ctx.guild.kick(user)

		kick= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		kick.add_field(name='User Affected:', value=f'`{user.name}``{user.discriminator}`', inline=True)
		kick.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		kick.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		kick.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		kick.add_field(name='Action Performed:', value='`Kick`', inline=True)
		kick.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		kick.set_thumbnail(url=user.avatar.url)
		#unban.timestamp = datetime.datetime.utcnow()

		await ctx.send(embed=kick)
 
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
"""

def setup(bot: commands.Bot):
	bot.add_cog(Mod(bot))
	