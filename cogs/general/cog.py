import nextcord, datetime
import nextcord.errors
from better_profanity import profanity
from nextcord.ext import commands, tasks
from nextcord.ext.commands import MissingPermissions
import aiohttp
from io import BytesIO
import asyncio
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

class General(commands.Cog, name="General"):
	"""Moderation commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="suggest")
	async def suggest(self, ctx, *, suggestion):
		await ctx.channel.purge(limit=1) # purge
		channel = nextcord.utils.get(ctx.guild.text_channel, name="suggestion")
		suggest = nextcord.Embed(title='New Suggestion!', description=f'{ctx.author.name} has suggested `{suggestion}`.')
		sugg = await channel.send(embed=suggest)
		await channel.send(f'^^ Suggestion ID: {sugg.id}')
		await sugg.add_reaction('✅')
		await sugg.add_reaction('❌')
  
	@commands.command(name="approve")
	async def approve(self, ctx, id:int=None, *, reason=None):
		if id is None:
			return
		channel = nextcord.utils.get(ctx.guild.text_channel, name='suggestion')
		if channel is None:
			return
		suggestionMsg = await channel.fetch_message(id)
		embed =nextcord.Embed(tittle=f'Suggestion has been approved', description=f' the suggestion id of "{suggestionMsg.id}" has been approved by {ctx.author.name} | reson: {reason}')
		await channel.send(embed=embed)

	@commands.command(name="deny")
	async def deny(self, ctx, id:int=None, *, reason=None):
		if id is None:
			return
		channel = nextcord.utils.get(ctx.guild.text_channel, name='suggestion')
		if channel is None:
			return
		suggestionMsg = await channel.fetch_message(id)
		embed =nextcord.Embed(tittle=f'Suggestion has been denied', description=f' the suggestion id of "{suggestionMsg.id}" has been denied by {ctx.author.name} | reson: {reason}')
		await channel.send(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(General(bot))
	