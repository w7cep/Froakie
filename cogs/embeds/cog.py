import nextcord
from nextcord.ext import commands


class Embeds(commands.Cog, name="Embeds"):
	"""Server Embed commands"""
	
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="forkbot_embed")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def forkbot_embed(self, ctx):
		forkbot = nextcord.Embed(title=f"__ForkBot.NET Release__", url="https://dev.azure.com/koigithub3088/SysBot_KoiFork/_build?definitionId=2&_a=summary", description="sys-botbase client for remote control automation of Nintendo Switch consoles. - Home · Koi-3088/ForkBot.NET Wiki")
		forkbot.set_thumbnail(url="https://cdn.mee6.xyz/guild-images/829558837609889804/ab3f13c97f829fe30ddcb9d8d4a9da4c7d17e2ebedf54ff60d51eb95947084b4.gif")
		forkbot.set_image(url="https://cdn-longterm.mee6.xyz/guild-images/829558837609889804/3edbea766c12a30e4540cb729a5bb50608a8866dbdcd18c55e25458d188c9784.png")
		forkbot.set_author(name=f"Greninja Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
		await ctx.send(embed=forkbot)

	@commands.command(name="server_navigation")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def server_navigation(self, ctx):
		navigation = nextcord.Embed(title="__Navigating the server__")
		navigation.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		navigation.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		navigation.add_field(name="#📃rules📃", value="• First channel you see, right after #👋welcome👋. \n• To get out and view the whole server, react to the rules with :thumbsup:", inline=False)
		navigation.add_field(name="#📡get-roles📡", value="• Pick up any roles you'd like, first category is the only that will receive pings. \n• Other categories are optional, not obligatory. \n• Pronouns are to be respected", inline=False)
		navigation.add_field(name="#🧾bot-rules🧾", value="• The rules of #🤖greninja-bot🤖 . \n• React with either 🤖 or 🎁  in #🧾bot-rules🧾 for access", inline=False)
		navigation.add_field(name="#tradecord", value="• Instructions: `!tci` / #❓tradecord-instructions❓.\n• Our version of Pokécord",inline=False)
		navigation.add_field(name="#🤖greninja-bot🤖", value="• Prefix:`$`.\n• Status: `!gbs`.\n• Instructions: `!gbi` / #❓greninja-bot-instructions❓ .\n• Generate any Pokémon in SwSh, illegals won't work (List of illegals `!illegal`.", inline=False)
		navigation.add_field(name="#📥request-a-mon📥", value="• Request any Pokémon, we'll provide a PK8 file asap", inline=False)
		navigation.add_field(name="#🛰auto-hosting🛰", value="• Where the host will post their raid info.\n\n#💭host-request💭  \n•Use `.suggest  <Your suggestion here>` to suggest a shiny den or max lair path.", inline=False)
		await ctx.send(embed=navigation)
def setup(bot: commands.Bot):
	bot.add_cog(Embeds(bot))
