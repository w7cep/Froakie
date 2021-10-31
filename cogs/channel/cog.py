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

class Sinner(commands.Converter):
	async def convert(self, ctx, argument):
		argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
		permission = argument.guild_permissions.manage_messages # can change into any permission
		if not permission: # checks if user has the permission
			return argument # returns user object
		else:
			raise commands.BadArgument("You cannot punish other staff members") # tells user that target is a staff member
class BannedUser(Converter):
	async def convert(self, ctx, arg):
		if ctx.guild.me.guild_permissions.ban_members:
			if arg.isdigit():
				try:
					return (await ctx.guild.fetch_ban(Object(id=int(arg)))).user
				except NotFound:
					raise BadArgument

		banned = [e.user for e in await ctx.guild.bans()]
		if banned:
			if (user := find(lambda u: str(u) == arg, banned)) is not None:
				return user
			else:
				raise BadArgument
class Channel(commands.Cog, name="Channel"):
	"""Channel commands"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot
		
		self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

	@commands.command(name="purge")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def purge(self, ctx, amount=5):
		"""Purge a number of messages in a channel"""
		await ctx.channel.purge(limit=amount + 1)
		embed = nextcord.Embed(
			title=f"{ctx.author.name} purged: {ctx.channel.name}",
			description=f"{amount} messages were cleared",
		)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed, delete_after=5)

	@commands.command(name="clean")
	@commands.has_role(829942684947841024)
	async def clean(self, ctx):
		"""Cleans the chat of the bot's messages."""
		def is_me(m):
			return m.author == self.bot.user
		await ctx.channel.trigger_typing()
		await ctx.message.channel.purge(limit=100, check=is_me)
  	
	@commands.command(name="lock")
	@commands.has_permissions(manage_channels=True)
	async def lock(self, ctx, *, channel: nextcord.TextChannel = None,reason = None):

		if channel == None:
			channel = ctx.channel
   
		await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=None, view_channel=None)
		await ctx.channel.trigger_typing()
		await channel.send(f"{channel.mention} has been locked 🔒")

	@commands.command(name="unlock")
	@commands.has_permissions(manage_channels=True)
	async def unlock(self, ctx, *, channel: nextcord.TextChannel = None,reason = None):

		if channel == None:
			channel = ctx.channel
   
		await channel.set_permissions(ctx.guild.default_role, send_messages=None, read_messages=None, view_channel=None)
		await ctx.channel.trigger_typing()
		await channel.send(f"{channel.mention} has been unlocked 🔓")
  
	'''	@lock.error
	async def lock_error(ctx, error):
		if isinstance(error,commands.CheckFailure):
			await ctx.send('You do not have permission to use this command!')'''
   
	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def new(self, ctx):
		"""Create new channels and categories.
		($$new category @role "name of category")
		($$new channel @role "name of channel")
		"""
		await ctx.channel.trigger_typing()
		await ctx.send("Invalid sub-command passed.")

	@new.command()
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def category(self, ctx, role: nextcord.Role, *, name):
		overwrites = {
		ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
		ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
		role: nextcord.PermissionOverwrite(read_messages=True)
		}
		category = await ctx.guild.create_category(name=name, overwrites=overwrites)
		await ctx.channel.trigger_typing()
		await ctx.send(f"Hey dude, I made {category.name} for ya!")

	@new.command()
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def channel(self, ctx, role: nextcord.Role, *, name):
		overwrites = {
		ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
		ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
		role: nextcord.PermissionOverwrite(read_messages=True)
		}
		channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites, category=self.bot.get_channel(709002944879656960))
		await ctx.channel.trigger_typing()
		await ctx.send(f"Hey dude, I made {channel.name} for ya!")

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def delete(self, ctx):
		"""Delete channels and categories.
		($$delete category @role "name of category")
		($$delete channel @role "name of channel")
		"""   
		await ctx.channel.trigger_typing()
		await ctx.send("Invalid sub-command passed.")

	@delete.command(name='category')
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def _category(self, ctx, category: nextcord.CategoryChannel, *, reason=None):
		await category.delete(reason=reason)
		await ctx.channel.trigger_typing()
		await ctx.send(f"Hey man! I deleted {category.name} for ya!")

	@delete.command(name='channel')
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def _channel(self, ctx, channel: nextcord.TextChannel=None, *, reason=None):
		channel = channel or ctx.channel
		await channel.delete(reason=reason)
		await ctx.channel.trigger_typing()
		await ctx.send(f"Hey man! I deleted {channel.name} for ya!")  

	@commands.command(aliases=['cs'], hidden=True)
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def channelstats(self, ctx):
		"""
		Sends a nice fancy embed with some channel stats
		"""
		channel = ctx.channel
		embed = nextcord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
		embed.add_field(name="Channel Id", value=channel.id, inline=False)
		embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
		embed.add_field(name="Channel Position", value=channel.position, inline=False)
		embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
		embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
		embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
		embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
		embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
		#!FIXME: embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
		await ctx.channel.trigger_typing()		
		await ctx.send(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(Channel(bot))

