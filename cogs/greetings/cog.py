from random import choice

import config
import nextcord
from nextcord.ext import commands, tasks
from nextcord.ext.commands import command


class GreetingsCog(commands.Cog, name="Greetings"):
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

	@commands.Cog.listener()
	async def on_member_join(self, member: nextcord.Member):
		"""Welcome members when they join"""
		guild = self.bot.get_guild(config.GUILD_ID)
		intro_channel = guild.get_channel(config.INTRO_CHANNEL_ID)
		rules_channel = guild.get_channel(config.RULES_CHANNEL_ID)
		bot_rules_channel = guild.get_channel(config.BOT_RULES_CHANNEL_ID)
		# don't welcome bots or members of other guilds the bot is in
		if member.bot or guild != member.guild:
			return
		# send welcome message
		await intro_channel.send(
			f"Welcome to **Greninja's Grotto**, {member.mention}!\n"
			f"Please read the rules in {rules_channel.mention} to gain access to the rest of the server!\n\nThen head over to {bot_rules_channel.mention} to gain access to the SysBot!"
		)
		# give the "unassigned" role
		await member.add_roles(guild.get_role(config.UNASSIGNED_ROLE_ID))

	@commands.Cog.listener()
	async def on_member_remove(self, member: nextcord.Member):
		"""Say goodbye to members."""
		guild = self.bot.get_guild(config.GUILD_ID)
		outro_channel = guild.get_channel(config.OUTRO_CHANNEL_ID)
		if member.bot or guild != member.guild:
			return
		await outro_channel.send(f"Peace! :middle_finger: {member.mention}")

	@command(name="hello", aliases=["hi"])
	async def say_hello(self, ctx):
		"""Say hi to the bot and it will say hi back."""
		await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!")

	@command(name="bye")
	async def say_bye(self, ctx):
		"""Say bye to the bot and it will say bye back."""
		await ctx.send(f"{choice(('Bye', 'Peace', 'See Ya', 'Later'))} {ctx.author.mention}!")

def setup(bot: commands.Bot):
	bot.add_cog(GreetingsCog(bot))
