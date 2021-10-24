import os

import aiohttp
import nextcord
import nextcord.ext
from nextcord.ext import commands

import config
from config import DISCORD_TOKEN


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

    async def startup():
        bot.session = aiohttp.ClientSession()

    bot.loop.create_task(startup())

    # run the bot
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()