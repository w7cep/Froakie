from nextcord.ext import commands

class PkmAutomation(commands.Cog, name="PkmAutomation"):
	"""Pokemon Automation Info Commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def arduino(self, ctx):
		"Arduino Commands"
		await ctx.channel.trigger_typing()
		await ctx.send("Invalid sub-command passed")
 
	@arduino.command(name="release")
	@commands.guild_only()
	async def release(self, ctx):
		"""Arduino Release Link"""
		await ctx.channel.trigger_typing()
		await ctx.send("https://github.com/PokemonAutomation/SwSh-Arduino/releases")
	
	@arduino.command(name="wiki")
	@commands.guild_only()
	async def wiki(self, ctx):
		"""Arduino Wiki."""
		await ctx.channel.trigger_typing()
		await ctx.send("https://github.com/PokemonAutomation/SwSh-Arduino/wiki")

	@arduino.command(name="beta")
	@commands.guild_only()
	async def beta(self, ctx):
		"""Arduino"""
		await ctx.channel.trigger_typing()
		await ctx.send("https://github.com/w7cep/Arduino-Beta")
  
	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def forkbot(self, ctx):
		"""Forkbot commands"""
		await ctx.channel.trigger_typing()
		await ctx.send("Invalid sub-command passed")
  
	@forkbot.command(name="release")
	@commands.guild_only()
	async def _release(self, ctx):
		"""ForkBot Release Link"""
		await ctx.channel.trigger_typing()
		await ctx.send("https://dev.azure.com/koigithub3088/SysBot_KoiFork/_build?definitionId=2&_a=summary")
	
	@forkbot.command(name="wiki")
	@commands.guild_only()
	async def _wiki(self, ctx):
		"""ForkBot Wiki"""
		await ctx.channel.trigger_typing()
		await ctx.send("https://github.com/Koi-3088/ForkBot.NET/wiki")

def setup(bot: commands.Bot):
	bot.add_cog(PkmAutomation(bot))
