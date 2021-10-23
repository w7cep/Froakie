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

class Mod(commands.Cog, name="Mod"):
	"""Moderation commands"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot

		self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

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

#this was in a cog
# The below code bans player.
	@commands.command()
	@commands.has_permissions(ban_members=True)
 	async def ban(self, ctx, member: nextcord.Member, *, reason=None):
	 		await member.ban(reason=reason)
	 		await ctx.send(f'User {member} has been kick')

# The below code unbans player.
	@commands.command()
	@commands.has_permissions(administrator=True)
  	async def unban(self, ctx, *, member):
	 		banned_users = await ctx.guild.bans()
	 		member_name, member_discriminator = member.split("#")

			for ban_entry in banned_users:
					user = ban_entry.user
			if (user.name, user.discriminator) == (member_name, member_discriminator):
					await ctx.guild.unban(user)
					await ctx.send(f'Unbanned {user.mention}')
					return

# The below code kicks player
	@commands.command()
	@commands.has_permissions(kick_members=True)
 	async def kick(self, ctx, member: nextcord.Member, *, reason=None):
			await member.kick(reason=reason)
			await ctx.send(f'User {member} has been kick')

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

def setup(bot: commands.Bot):
	bot.add_cog(Mod(bot))

