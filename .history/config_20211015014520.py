import os

import settings


# Bot setup
PREFIX = "$$"
BOT_NAME = "Greninja Mod"
BOT_TOKEN = settings.DISCORD_TOKEN

# Discord Guild ID
GUILD_ID = settings.GUILD_ID

# Discord Channel IDs
INTRO_CHANNEL_ID = settings.INTRO_CHANNEL_ID
RULES_CHANNEL_ID = int(os.getenv("RULES_CHANNEL_ID
BOT_LOG_CHANNEL_ID = int(os.getenv("BOT_LOG_CHANNEL_ID

# Discord Role IDs
TRADECORD_ROLE_ID = int(os.getenv("TRADECORD_ROLE_ID
FROGADIER_ROLE_ID = int(os.getenv("FROGADIER_ROLE_ID
#SUBSCRIBER_ROLE_ID = int(os.getenv("SUBSCRIBER_ROLE_ID
MEMBER_ROLE_ID = int(os.getenv("MEMBER_ROLE_ID
UNASSIGNED_ROLE_ID = settings.UNASSIGNED_ROLE_ID


# Discord Message IDs
RULES_MESSAGE_ID = int(os.getenv("RULES_MESSAGE_ID", ""))


