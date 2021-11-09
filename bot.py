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

	activity = nextcord.Activity(type=nextcord.ActivityType.listening, name=f"{config.BOT_STATUS}")

	bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, activity=activity)

	# boolean that will be set to true when views are added
	bot.persistent_views_added = False

	@bot.event
	async def on_ready():
		member_count = 0
		guild_string = ""
		for g in bot.guilds:
			guild_string += f"{g.name} - {g.id} - Members: {g.member_count}\n"
			member_count += g.member_count
		print(f"Bot: '{bot.user.name}' has connected to Discord, active on {len(bot.guilds)} guilds:\n{guild_string}")
		print(f"nextcord API version: {nextcord.__version__}")
		print(f"Python version: {platform.python_version()}")
		print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
		channel = bot.get_channel(907496711872729128) #  Gets channel from internal cache
		await channel.send(f"{bot.user.name} is connected to {len(bot.guilds)} guilds:\n{guild_string}\nnextcord API version: {nextcord.__version__}\nPython version: {platform.python_version()}\n Running on: {platform.system()} {platform.release()} ({os.name})") #  Sends message to channel
	# load all cogs
	for folder in os.listdir("cogs"):
		if os.path.exists(os.path.join("cogs", folder, "cog.py")):
			bot.load_extension(f"cogs.{folder}.cog")

	async def startup():
		bot.session = aiohttp.ClientSession()

	bot.loop.create_task(startup())

	# run the bot
	bot.run(config.BOT_TOKEN)

if __name__ == "__main__":
	main()
