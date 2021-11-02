import asyncio
import nextcord, datetime
from nextcord.ext import commands, tasks
from better_profanity import profanity

profanity.load_censor_words_from_file("./data/profanity.txt")
class ServerMod(commands.Cog, name="ServerMod"):
	"""Greeting commands"""
	
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self._last_member = None
		self.bot_reminder.start()

	@tasks.loop(hours=8)  # you can even use hours and minutes
	async def bot_reminder(self):
		print("Sending message")
		channel = self.bot.get_channel(843271842931933224)
		await channel.send("**Reminder**\n\nUsing the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n\nPlease don't delete messages. Even when it's a mistake.\nMakes trouble-shooting difficult.\n\nBot access will be revoked for multiple offenders.")

	@bot_reminder.before_loop
	async def before_bot_reminder(self):
		print('waiting...')
		await self.bot.wait_until_ready()

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def profanity(self, ctx):
		await ctx.send("Invalid sub-command specified")
	
	@profanity.command(name="add")
	@commands.has_role(829942684947841024)
	async def add(self, ctx, *words):
		'''Add cuss word to file.'''
		with open("./data/profanity.txt", "a", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in words]))

		profanity.load_censor_words_from_file("./data/profanity.txt")
		await ctx.channel.trigger_typing()
		await ctx.send("Action complete.")

	@profanity.command(name="del")
	@commands.has_role(829942684947841024)
	async def remove_profanity(self, ctx, *words):
		'''Delete cuss word from file.'''
		with open("./data/profanity.txt", "r", encoding="utf-8") as f:
			stored = [w.strip() for w in f.readlines()]

		with open("./data/profanity.txt", "w", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in stored if w not in words]))

		profanity.load_censor_words_from_file("./data/profanity.txt")
		await ctx.channel.trigger_typing()
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

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def embed(self, ctx):
		await ctx.send("Invalid sub-command specified")

	@embed.command(name="sysbot_access")
	@commands.is_owner()
	async def sysbot_access(self, ctx):
		"""Sysbot access embed."""
		embed=nextcord.Embed(title="__**Sysbot Access**__", 
							description=f"Check out <#868914000572846120> for access to the sysbot.\n")
		embed.add_field(name="__**Reminder**__", value="Don't delete messages in the bot channel. It makes it harder to trouble shoot problems with the bot.")
	   
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_author(name="Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
		embed.set_footer(text="Bot is running v1.0.0") 
		await ctx.channel.trigger_typing() 
		await ctx.send(embed=embed)

	@embed.command(name="forkbot_release")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def forkbot_release(self, ctx):
		forkbot = nextcord.Embed(title=f"__ForkBot.NET Release__", url="https://dev.azure.com/koigithub3088/SysBot_KoiFork/_build?definitionId=2&_a=summary", description="sys-botbase client for remote control automation of Nintendo Switch consoles. - Home · Koi-3088/ForkBot.NET Wiki")
		forkbot.set_thumbnail(url="https://cdn.mee6.xyz/guild-images/829558837609889804/ab3f13c97f829fe30ddcb9d8d4a9da4c7d17e2ebedf54ff60d51eb95947084b4.gif")
		forkbot.set_image(url="https://cdn-longterm.mee6.xyz/guild-images/829558837609889804/3edbea766c12a30e4540cb729a5bb50608a8866dbdcd18c55e25458d188c9784.png")
		forkbot.set_author(name=f"Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
		await ctx.send(embed=forkbot)

	@embed.command(name="server_navigation")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def server_navigation(self, ctx):
		version = "1.1.0"
		navigation = nextcord.Embed(title="__Navigating the server__")
		navigation.set_footer(text=f"{version}")
		navigation.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		navigation.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		navigation.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		navigation.add_field(name="#📃rules📃", value="• First channel you see, right after #👋welcome👋. \n• To get out and view the whole server, react to the rules with :thumbsup:", inline=False)
		navigation.add_field(name="#📡get-roles📡", value="• Pick up any roles you'd like, first category is the only that will receive pings. \n• Other categories are optional, not obligatory. \n• Pronouns are to be respected", inline=False)
		navigation.add_field(name="#🧾bot-rules🧾", value="• The rules of #🤖greninja-bot🤖 . \n• React with either 🤖 or 🎁  in #🧾bot-rules🧾 for access", inline=False)
		navigation.add_field(name="#tradecord", value="• Instructions: `!tci` / #❓tradecord-instructions❓.\n• Our version of Pokécord",inline=False)
		navigation.add_field(name="#🤖greninja-bot🤖", value="• Prefix:`$`.\n• Instructions: #❓greninja-bot-instructions❓.\n• Generate any Pokémon in SwSh, illegals won't work (List of illegals `!illegal`.", inline=False)
		navigation.add_field(name="#📥request-a-mon📥", value="• Request any Pokémon, we'll provide a PK8 file asap", inline=False)
		navigation.add_field(name="#🛰auto-hosting🛰", value="• Where the host will post their raid info.\n\n#💭host-request💭  \n•Use `.suggest  <Your suggestion here>` to suggest a shiny den or max lair path.", inline=False)
		navigation.add_field(name="#💭host-request💭", value="• Use `!request <Your suggestion here>` to request a Den or Max Lair Path.", inline=False)
		navigation.add_field(name="__**Support**__", value="• Use `!support` to open a support channel\n• An @💪Admin💪 or @💪Moderator💪 will be with you shortly.")
		await ctx.send(embed=navigation)

def setup(bot: commands.Bot):
	bot.add_cog(ServerMod(bot))
