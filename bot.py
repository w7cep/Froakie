import os

import aiohttp
import nextcord
import nextcord.ext
from nextcord.ext import commands, tasks
import platform
import config

# TODO: #1 Fine tune command permissions.
# TODO: #2 Delete every excess space / Convert files with space indents to tabs.

def main():
	# allows privledged intents for monitoring members joining, roles editing, and role assignments
	intents = nextcord.Intents.all()

	activity = nextcord.Activity(type=nextcord.ActivityType.listening, name=f"{config.PREFIX}help | discord.gg/dm7gSAT68d")

	bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, activity=activity)

	# boolean that will be set to true when views are added
	bot.persistent_views_added = False

	@bot.event
	async def on_ready():
		print(f"{bot.user.name} has connected to Discord.")
		print()
		member_count = 0
		guild_string = ""
		for g in bot.guilds:
			guild_string += f"{g.name} - {g.id} - Members: {g.member_count}\n"
			member_count += g.member_count
		print(f"Bot: '{bot.user.name}' has connected, active on {len(bot.guilds)} guilds:\n{guild_string}")
		print(f"nextcord API version: {nextcord.__version__}")
		print(f"Python version: {platform.python_version()}")
		print(f"Running on: {platform.system()} {platform.release()} ({os.name})")

	# load all cogs
	for folder in os.listdir("cogs"):
		if os.path.exists(os.path.join("cogs", folder, "cog.py")):
			print(f"Loading cog {folder}")
			bot.load_extension(f"cogs.{folder}.cog")
			print(f"Loaded cog {folder}")
	async def startup():
		bot.session = aiohttp.ClientSession()

	bot.loop.create_task(startup())

	# run the bot
	bot.run(config.BOT_TOKEN)

if __name__ == "__main__":
	main()
