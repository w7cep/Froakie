import nextcord
from nextcord.ext import commands
import config

class Pokemon(commands.Cog, name="Pokemon"):
	"""Instruction commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def pokemon(self, ctx):
		await ctx.send("Invalid sub-command specified")
  
	@pokemon.command(name="types")
	async def type_advantage(self, ctx):
		"""Pokemon type advantages."""
		await ctx.channel.trigger_typing()
		await ctx.send(file=nextcord.File("assets/imgs/info/weakness.jpg"))

	@pokemon.command(name="request")
	async def request(self, ctx, *, reason = None):
		"""Request a den or max lair path"""
		bot = self.bot.user
		user = ctx.author
		channel = await ctx.guild.fetch_channel(config.SUGGESTION_CHANNEL_ID)
		if reason is None:
			await ctx.send("Please suggest a 'Den' or 'Max Lair Path'.")
		else:
			embed = nextcord.Embed(title=f"{user} requested support.", description= "An admin will be with you shortly...", color=0x00ff00)
			embed.add_field(name="Suggestion", value=f"{reason}")
			embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
			embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
			embed.set_footer(text=f"{user.name}{user.discriminator}--ID:{user.id}", icon_url=user.avatar.url)
			embed.set_author(name=bot.name, icon_url=bot.avatar.url)
			await ctx.channel.trigger_typing()
			await channel.send(embed=embed)

	@commands.command(name="lair_suggest")
	async def lair_suggest(self, ctx, *, suggestion):
		await ctx.channel.purge(limit=1) # purge
		channel = await ctx.guild.fetch_channel(config.LAIR_SUGGESTION_CHANNEL_ID)
		suggest = nextcord.Embed(title='New Suggestion!', description=f'{ctx.author.name} has suggested `{suggestion}`.')
		sugg = await channel.send(embed=suggest)
		await sugg.add_reaction('✅')
		await sugg.add_reaction('❌')
		suggest2 = nextcord.Embed(title='New Suggestion!', description=f'{ctx.author.name} has suggested `{suggestion}`.')
		suggest2.add_field(name='Msg ID:', value=f'{sugg.id}', inline=False)
		await sugg.edit(embed=suggest2)
  
	@commands.command(name="lair_approve")
	async def lair_approve(self, ctx, id:int=None, *, reason=None):
		await ctx.channel.purge(limit=1)
		if id is None:
			return
		channel = await ctx.guild.fetch_channel(config.LAIR_SUGGESTION_CHANNEL_ID)
		if channel is None:
			return
		suggestionMsg = await channel.fetch_message(id)
		embed =nextcord.Embed(title=f'Suggestion has been approved', description=f'Suggestion `{suggestionMsg.id}` has been approved by {ctx.author.name} | reason: {reason}')
		Msg = await channel.send(embed=embed)
		await Msg.add_reaction('✅')
  
	@commands.command(name="lair_deny")
	async def lair_deny(self, ctx, id:int=None, *, reason=None):
		await ctx.channel.purge(limit=1)
		if id is None:
			return
		channel = await ctx.guild.fetch_channel(config.LAIR_SUGGESTION_CHANNEL_ID)
		if channel is None:
			return
		suggestionMsg = await channel.fetch_message(id)
		embed =nextcord.Embed(title=f'Suggestion has been denied', description=f'Suggestion `{suggestionMsg.id}` has been denied by {ctx.author.name}')
		embed.add_field(name='reason:', value=f'{reason}')
		Msg = await channel.send(embed=embed)
		await Msg.add_reaction('❌')

	@commands.command(name="den_suggest")
	async def den_suggest(self, ctx, *, suggestion):
		await ctx.channel.purge(limit=1) # purge
		channel = await ctx.guild.fetch_channel(config.DEN_SUGGESTION_CHANNEL_ID)
		suggest = nextcord.Embed(title='New Suggestion!', description=f'{ctx.author.name} has suggested `{suggestion}`.')
		sugg = await channel.send(embed=suggest)
		await sugg.add_reaction('✅')
		await sugg.add_reaction('❌')
		suggest2 = nextcord.Embed(title='New Suggestion!', description=f'{ctx.author.name} has suggested `{suggestion}`.')
		suggest2.add_field(name='Msg ID:', value=f'{sugg.id}', inline=False)
		await sugg.edit(embed=suggest2)
  
	@commands.command(name="den_approve")
	async def den_approve(self, ctx, id:int=None, *, reason=None):
		await ctx.channel.purge(limit=1)
		if id is None:
			return
		channel = await ctx.guild.fetch_channel(config.DEN_SUGGESTION_CHANNEL_ID)
		if channel is None:
			return
		suggestionMsg = await channel.fetch_message(id)
		embed =nextcord.Embed(title=f'Suggestion has been approved', description=f'Suggestion `{suggestionMsg.id}` has been approved by {ctx.author.name} | reason: {reason}')
		Msg = await channel.send(embed=embed)
		await Msg.add_reaction('✅')
  
	@commands.command(name="den_deny")
	async def den_deny(self, ctx, id:int=None, *, reason=None):
		await ctx.channel.purge(limit=1)
		if id is None:
			return
		channel = await ctx.guild.fetch_channel(config.DEN_SUGGESTION_CHANNEL_ID)
		if channel is None:
			return
		suggestionMsg = await channel.fetch_message(id)
		embed =nextcord.Embed(title=f'Suggestion has been denied', description=f'Suggestion `{suggestionMsg.id}` has been denied by {ctx.author.name}')
		embed.add_field(name='reason:', value=f'{reason}')
		Msg = await channel.send(embed=embed)
		await Msg.add_reaction('❌')



def setup(bot: commands.Bot):
	bot.add_cog(Pokemon(bot))
