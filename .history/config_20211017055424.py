import os
from dotenv.main import load_dotenv

load_dotenv()

# Bot setup
PREFIX = "$$"
BOT_NAME = "Greninja Mod"
BOT_TOKEN = os.getenv("DISCORD_TOKEN", "")

# Discord Guild ID
GUILD_ID = int(os.getenv("GUILD_ID", ""))

# Discord Channel IDs
INTRO_CHANNEL_ID = int(os.getenv("INTRO_CHANNEL_ID", ""))
RULES_CHANNEL_ID = int(os.getenv("RULES_CHANNEL_ID", ""))
BOT_LOG_CHANNEL_ID = int(os.getenv("BOT_LOG_CHANNEL_ID", ""))
BOT_RULES_CHANNEL_ID = int(os.getenv("BOT_RULES_CHANNEL_ID", ""))

# Discord Role IDs
FROGADIER_ROLE_ID = int(os.getenv("FROGADIER_ROLE_ID", ""))
TRADECORD_ROLE_ID = int(os.getenv("TRADECORD_ROLE_ID", ""))
MEMBER_ROLE_ID = int(os.getenv("MEMBER_ROLE_ID", ""))
UNASSIGNED_ROLE_ID = int(os.getenv("UNASSIGNED_ROLE_ID", ""))



# Discord Message IDs
RULES_MESSAGE_ID = int(os.getenv("RULES_MESSAGE_ID", ""))

