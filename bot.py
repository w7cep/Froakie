import os

import aiohttp
import nextcord
import nextcord.ext
from nextcord.ext import commands, tasks

import config

def main():
	# allows privledged intents for monitoring members joining, roles editing, and role assignments
	intents = nextcord.Intents.all()

	activity = nextcord.Activity(type=nextcord.ActivityType.listening, name=f"{config.PREFIX}help")

	bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, activity=activity)

	# boolean that will be set to true when views are added
	bot.persistent_views_added = False

	@bot.event
	async def on_ready():
		print(f"{bot.user.name} has connected to Discord.")

	# load all cogs
	for folder in os.listdir("cogs"):
		if os.path.exists(os.path.join("cogs", folder, "cog.py")):
			bot.load_extension(f"cogs.{folder}.cog")

	'''	@tasks.loop(hours=6)  # you can even use hours and minutes
	async def send_message():
		await bot.get_channel(843271842931933224).send("**Reminder**\n\nUsing the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n\nPlease don't delete messages. Even when it's a mistake.\nMakes trouble-shooting difficult.\n\nBot access will be revoked for multiple offenders.")'''
	
	async def startup():
		bot.session = aiohttp.ClientSession()

	bot.loop.create_task(startup())
	
	# run the bot
	bot.run(config.BOT_TOKEN)

if __name__ == "__main__":
	main()