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

	@commands.command(
		name="purge",
		description="A command which purges the channel it is called in",
		usage="[amount]",
	)
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def purge(self, ctx, amount=5):
		await ctx.channel.purge(limit=amount + 1)
		embed = nextcord.Embed(
			title=f"{ctx.author.name} purged: {ctx.channel.name}",
			description=f"{amount} messages were cleared",
		)
		await ctx.send(embed=embed, delete_after=15)

	@commands.command(name="clean")
	@commands.has_permissions(administrator=True)
	async def clean(self, ctx):
		"""Cleans the chat of the bot's messages."""
		def is_me(m):
			return m.author == self.bot.user
		await ctx.message.channel.purge(limit=100, check=is_me)
		
	@commands.command(
		name="lockdown",
		description="A command to lock or unlock a channel.",
		usage="[@channel]",
	)
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def lockdown(self, ctx, channel: nextcord.TextChannel=None):
		if channel is None:
			channel = ctx.channel

		if ctx.guild.default_role not in channel.overwrites:
			overwrites = {
			ctx.guild.default_role: nextcord.PermissionOverwrite(send_messages=False)
			}
			await channel.edit(overwrites=overwrites)
			await ctx.send(f"I have put `{channel.name}` on lockdown.")
		elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
			overwrites = channel.overwrites[ctx.guild.default_role]
			overwrites.send_messages = False
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
			await ctx.send(f"I have put `{channel.name}` on lockdown.")
		else:
			overwrites = channel.overwrites[ctx.guild.default_role]
			overwrites.send_messages = True
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
			await ctx.send(f"I have removed `{channel.name}` from lockdown.")

	@commands.Cog.listener()
	async def on_message(self, message):
		def _check(m):
			return (m.author == message.author
					and len(m.mentions)
					and (datetime.utcnow()-m.created_at).seconds < 60)

		if profanity.contains_profanity(message.content):
			await message.delete()
			await message.channel.send("You can't use that word here.", delete_after=10)
   
	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_guild_permissions(manage_channels=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def new(self, ctx):
		"""Create new channels and categories.
		($$new category @role "name of category")
		($$new channel @role "name of channel")
		"""
		await ctx.send("Invalid sub-command passed.")

	@new.command()
	@commands.guild_only()
	@commands.has_guild_permissions(manage_channels=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def category(self, ctx, role: nextcord.Role, *, name):
		overwrites = {
		ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
		ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
		role: nextcord.PermissionOverwrite(read_messages=True)
		}
		category = await ctx.guild.create_category(name=name, overwrites=overwrites)
		await ctx.send(f"Hey dude, I made {category.name} for ya!")

	@new.command()
	@commands.guild_only()
	@commands.has_guild_permissions(manage_channels=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def channel(self, ctx, role: nextcord.Role, *, name):
		overwrites = {
		ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
		ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
		role: nextcord.PermissionOverwrite(read_messages=True)
		}
		channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites, category=self.bot.get_channel(709002944879656960))
		await ctx.send(f"Hey dude, I made {channel.name} for ya!")

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_guild_permissions(manage_channels=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def delete(self, ctx):
		"""Delete channels and categories.
		($$delete category @role "name of category")
		($$delete channel @role "name of channel")
		"""   
		await ctx.send("Invalid sub-command passed.")

	@delete.command(name='category')
	@commands.guild_only()
	@commands.has_guild_permissions(manage_channels=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def _category(self, ctx, category: nextcord.CategoryChannel, *, reason=None):
		await category.delete(reason=reason)
		await ctx.send(f"Hey man! I deleted {category.name} for ya!")

	@delete.command(name='channel')
	@commands.guild_only()
	@commands.has_guild_permissions(manage_channels=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def _channel(self, ctx, channel: nextcord.TextChannel=None, *, reason=None):
		channel = channel or ctx.channel
		await channel.delete(reason=reason)
		await ctx.send(f"Hey man! I deleted {channel.name} for ya!")  

def setup(bot: commands.Bot):
	bot.add_cog(Channel(bot))
