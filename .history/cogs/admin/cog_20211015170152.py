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
class AdminCog(commands.Cog, name="Admin"):
	"""Admin commands"""

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
		
	@commands.command(name="role")
	@commands.has_permissions(administrator=True) #permissions
	async def role(self, ctx, user : nextcord.Member, *, role : nextcord.Role):
		'''Give role to member.'''
		if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
			return await ctx.send('**:x: | That role is above your top role!**')
		if role in user.roles:
			await user.remove_roles(role) #removes the role if user already has
			await ctx.send(f"Removed {role} from {user.mention}") 
		else:
			await user.add_roles(role) #adds role if not already has it
			await ctx.send(f"Added {role} to {user.mention}")
			
	@role.error
	async def role_error(self, ctx, error):
		if isinstance(error, MissingPermissions):
			await ctx.send('**:x: | You do not have permission to use this command!**')
			
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
			
	@commands.command(name="memberinfo", aliases=["mi"]) 
	@commands.has_permissions(administrator=True)
	@commands.guild_only()
	async def memberinfo(self, ctx, *, user: nextcord.Member = None):
		
		"""
		Get information about you, or a specified user.
		`$$mi <user>`
		`user`: The user who you want information about. Can be an ID, mention or name.
		"""

		if user is None:
			user = ctx.author
			
		embed = nextcord.Embed(
			
			title=f"{user.name}'s Stats and Information.",
			
		)
		embed.set_footer(text=f"ID: {user.id}")
		embed.set_thumbnail(url=user.avatar.url(format="png"))
		embed.add_field(name="__**General information:**__", value=f"**Discord Name:** {user}\n"
																   f"**Account created:** {user.created_at.__format__('%A %d %B %Y at %H:%M')}", inline=False)        
		embed.add_field(name="__**Server-related information:**__", value=f"**Nickname:** {user.nick}\n"
																		  f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
																		  f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}")
		return await ctx.send(embed=embed)

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

	@commands.command(name="cmd")
	@commands.has_permissions(administrator=True)
	@commands.guild_only()
	async def cmd(self, ctx):

		"""Test Embed."""
		
		version = "v1.0.0"
		
		embed = nextcord.Embed(
			title="__**Server Commands**__",
			description="List of all server commands.",
			colour=nextcord.Colour.blue()
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_author(name="Greninja Mod", icon_url="https://cdn.discordapp.com/avatars/866572422438060052/cb32b40409c7df4d147c400582f939ac.webp?size=4096")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		###########################################################################################################################
		embed.add_field(name="__**Admin Commands:**__", value=f"**$$clean** : Cleans the chat of bot messages.\n"
												f"**$$role** : Give role to member.\n"
												f"**$$memberinfo, $$mi** : Get information about a member.\n"
												f"**$$addprofanity** : Add cuss word to file.\n" 
												f"**$$delprofanity** : Delete cuss word from file.\n"
												f"**$$cmd** : List all bot commands."
												f"**$$emojiinfo** : Get info about an emoji.\n"
												f"**$$channelstats, $$cs** : Get channel stats.\n" 
												f"**$$new category <role> <name>** : Create a new category.\n"
												f"**$$new channel <role> <name>** : Create a new channel.\n" 
												f"**$$delete category <role> <name>** : Create a new category.\n"
												f"**$$delete channel <role> <name>** : Create a new channel.\n" 
												f"**$$lockdown** : Lock or Unlock a channel.\n", inline=False)
		
		embed.add_field(name="__**General Commands:**__", value=f"**$$hello** : Say hello to the bot.\n"
												f"**$$bye** : Say bye to the bot.\n"
												f"**$$slap** : Slap another member.\n"
												f"**$$fact** : Get a fact about an animal.\n"
												f"**$$stats** : Get bot stats.", inline=False)                                                    
		embed.set_footer(text=f"Bot is running {version}")
		await ctx.send(embed=embed)
		
	@commands.command(name="emojiinfo", aliases=["ei"])
	@commands.has_permissions(administrator=True)
	async def emoji_info(self, ctx, emoji: nextcord.Emoji = None):
		if not emoji:
					await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

		try:
					emoji = await emoji.guild.fetch_emoji(emoji.id)
		except nextcord.NotFound:
					await ctx.send("I could not find this emoji in the given guild.")

		is_managed = "Yes" if emoji.managed else "No"
		is_animated = "Yes" if emoji.animated else "No"
		requires_colons = "Yes" if emoji.require_colons else "No"
		creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
		can_use_emoji = (
			"Everyone"
			if not emoji.roles
			else " ".join(role.name for role in emoji.roles)
		)

		description = f"""
		**General:**
		**- Name:** {emoji.name}
		**- Id:** {emoji.id}
		**- URL:** [Link To Emoji]({emoji.url})
		**- Author:** {emoji.user.name}
		**- Time Created:** {creation_time}
		**- Usable by:** {can_use_emoji}
		
		**Other:**
		**- Animated:** {is_animated}
		**- Managed:** {is_managed}
		**- Requires Colons:** {requires_colons}
		**- Guild Name:** {emoji.guild.name}
		**- Guild Id:** {emoji.guild.id}
		"""

		embed = nextcord.Embed(
		title=f"**Emoji Information for:** `{emoji.name}`",
		description=description,
		colour=0xADD8E6,
		)
		embed.set_thumbnail(url=emoji.url)
		await ctx.send(embed=embed)
		
	@commands.command(aliases=['cs'])
	@commands.has_permissions(administrator=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def channelstats(self, ctx):
		"""
		Sends a nice fancy embed with some channel stats
		"""
		channel = ctx.channel
		embed = nextcord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",)
		embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
		embed.add_field(name="Channel Id", value=channel.id, inline=False)
		embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
		embed.add_field(name="Channel Position", value=channel.position, inline=False)
		embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
		embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
		embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
		embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
		embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
		embed.add_field(name="Channel Hash", value=hash(channel), inline=False)

		await ctx.send(embed=embed)

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



	@commands.command(name="type")
	async def type(self, ctx):
		"""Type advantages."""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/info/weakness.jpg"))
		
def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))

