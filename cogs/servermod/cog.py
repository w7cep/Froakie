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
		self.send_message.start()

	@tasks.loop(minutes=10)  # you can even use hours and minutes
	async def send_message(self):
		print("Sending message")
		await self.bot.get_channel(904434133793656932).send("**Reminder**\n\nUsing the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n\nPlease don't delete messages. Even when it's a mistake.\nMakes trouble-shooting difficult.\n\nBot access will be revoked for multiple offenders.")

	@send_message.before_loop
	async def before_printer(self):
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

	@commands.command(name="say")
	@commands.is_owner()
	async def say(self, ctx, channel:nextcord.TextChannel, *, message):
		"""Make the bot say something in the specified channel."""
		if channel is not None:
			await ctx.channel.trigger_typing()
			await channel.send(message)

	@commands.command(name="say_embed")
	@commands.is_owner()
	async def say_embed(self, ctx, channel:nextcord.TextChannel, *, message):
		"""Make the bot say something in the specified channel as an embed."""
		if channel is not None:
			embed= nextcord.Embed(description=f"{message}")
			embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
			embed.set_image(url="https://cdn.discordapp.com/attachments/901687898452131860/902400527621566504/greninja_banner.jpg")
			embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
			embed.set_author(name=f"Greninja Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
		await ctx.channel.trigger_typing()
		await channel.send(embed=embed)

	@commands.command(name="echo")
	@commands.has_role(829942684947841024)
	async def echo(self, ctx):
		"""Have the bot echo something and hide the evidence."""
		await ctx.message.delete()
		embed = nextcord.Embed(
			title="Please tell me what you want me to repeat!",
			description="This request will timeout after 1 minute.",
		)
		await ctx.channel.trigger_typing()
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
				await ctx.channel.trigger_typing()
				await ctx.send(msg.content)
		except asyncio.TimeoutError:
			await sent.delete()
			await ctx.channel.trigger_typing()
			await ctx.send("Cancelling", delete_after=10)

	@commands.command(name="emojiinfo", aliases=["ei"])
	@commands.has_role(829942684947841024)
	async def emoji_info(self, ctx, emoji: nextcord.Emoji = None):
		"""Display information about an emoji in the server."""
		if not emoji:
					await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

		try:
					emoji = await emoji.guild.fetch_emoji(emoji.id)
		except nextcord.NotFound:
					await ctx.channel.trigger_typing()
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
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)


def setup(bot: commands.Bot):
	bot.add_cog(ServerMod(bot))
