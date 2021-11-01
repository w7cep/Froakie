import nextcord
from nextcord.ext import commands



class Embeds(commands.Cog, name="Embeds"):
	"""Server Embed commands"""
	
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.commands(name="forkbot_embed")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def forkbot_embed(self, ctx):
		forkbot = nextcord.Embed(title=f"__ForkBot.NET Release__", url="https://dev.azure.com/koigithub3088/SysBot_KoiFork/_build?definitionId=2&_a=summary", description="sys-botbase client for remote control automation of Nintendo Switch consoles. - Home · Koi-3088/ForkBot.NET Wiki"
		)
		forkbot.set_thumbnail(url="https://cdn.mee6.xyz/guild-images/829558837609889804/ab3f13c97f829fe30ddcb9d8d4a9da4c7d17e2ebedf54ff60d51eb95947084b4.gif")
		forkbot.set_image(url="https://cdn-longterm.mee6.xyz/guild-images/829558837609889804/3edbea766c12a30e4540cb729a5bb50608a8866dbdcd18c55e25458d188c9784.png")
		forkbot.set_author(name=f"Greninja Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
		await ctx.send(embed=forkbot)

def setup(bot: commands.Bot):
	bot.add_cog(Embeds(bot))
