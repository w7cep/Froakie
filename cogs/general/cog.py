import nextcord, datetime
import nextcord.errors
from better_profanity import profanity
from nextcord.ext import commands, tasks
from nextcord.ext.commands import MissingPermissions
import aiohttp
from io import BytesIO
import asyncio
import config
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
	"""Testing Commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="tmp_mute")
	@commands.has_permissions(manage_messages=True)
	async def tmp_mute(self, ctx, user: nextcord.Member, time):
		muted_role=nextcord.utils.get(ctx.guild.roles, name="Muted")
		time_convert = {"s":1, "m":60, "h":3600,"d":86400}
		tempmute= int(time[0]) * time_convert[time[-1]]
		await ctx.message.delete()
		await user.add_roles(muted_role)
		embed = nextcord.Embed(description= f"✅ **{user.display_name}#{user.discriminator} muted successfully**", color=nextcord.Color.green())
		await ctx.send(embed=embed, delete_after=5)
		await asyncio.sleep(tempmute)
		await user.remove_roles(muted_role) 
		await ctx.send(f"{user.display_name}${user.discriminator} has be unmuted!")
  
	@commands.command(name="suggest")
	async def suggest(self, ctx, *, suggestion):
		await ctx.channel.purge(limit=1) # purge
		channel = await ctx.guild.fetch_channel(config.SUGGESTION_CHANNEL_ID)
		suggest = nextcord.Embed(title='New Suggestion!', description=f'{ctx.author.name} has suggested `{suggestion}`.')
		sugg = await channel.send(embed=suggest)
		await sugg.add_reaction('✅')
		await sugg.add_reaction('❌')
		suggest2 = nextcord.Embed(title='New Suggestion!', description=f'{ctx.author.name} has suggested `{suggestion}`.')
		suggest2.add_field(name='Msg ID:', value=f'{sugg.id}', inline=False)
		await sugg.edit(embed=suggest2)
  
	@commands.command(name="approve")
	async def approve(self, ctx, id:int=None, *, reason=None):
		await ctx.channel.purge(limit=1)
		if id is None:
			return
		channel = await ctx.guild.fetch_channel(config.SUGGESTION_CHANNEL_ID)
		if channel is None:
			return
		suggestionMsg = await channel.fetch_message(id)
		embed =nextcord.Embed(title=f'Suggestion has been approved', description=f'Suggestion `{suggestionMsg.id}` has been approved by {ctx.author.name} | reason: {reason}')
		Msg = await channel.send(embed=embed)
		await Msg.add_reaction('✅')
  
	@commands.command(name="deny")
	async def deny(self, ctx, id:int=None, *, reason=None):
		await ctx.channel.purge(limit=1)
		if id is None:
			return
		channel = await ctx.guild.fetch_channel(config.SUGGESTION_CHANNEL_ID)
		if channel is None:
			return
		suggestionMsg = await channel.fetch_message(id)
		embed =nextcord.Embed(title=f'Suggestion has been denied', description=f'Suggestion `{suggestionMsg.id}` has been denied by {ctx.author.name}')
		embed.add_field(name='reason:', value=f'{reason}')
		Msg = await channel.send(embed=embed)
		await Msg.add_reaction('❌')


def setup(bot: commands.Bot):
	bot.add_cog(General(bot))
	