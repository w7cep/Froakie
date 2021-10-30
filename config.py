import os
from dotenv.main import load_dotenv

load_dotenv()

# Bot setup
PREFIX = "!"
BOT_NAME = "Greninja Mod"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Discord Guild ID
GUILD_ID = int(os.getenv("GUILD_ID", ""))

WATCHING_STATUS = "for infringements"

MUTED_ROLE_NAME = "Muted"
MOD_LOG_CHANNEL_NAME = "greninja-mod-logs"


MODLOG_COLORS = {"BAN": 0xeb4034, "MUTE": 0xeda239, "UNMUTE": 0x56c470, "UNBAN": 0x4fb09e, "KICK": 0x559ced}

# Discord Channel IDs
INTRO_CHANNEL_ID = int(os.getenv("INTRO_CHANNEL_ID", ""))
RULES_CHANNEL_ID = int(os.getenv("RULES_CHANNEL_ID", ""))
BOT_LOG_CHANNEL_ID = int(os.getenv("BOT_LOG_CHANNEL_ID", ""))
BOT_RULES_CHANNEL_ID = int(os.getenv("BOT_RULES_CHANNEL_ID", ""))
OUTRO_CHANNEL_ID = int(os.getenv("OUTRO_CHANNEL_ID", ""))
SUGGESTION_CHANNEL_ID = int(os.getenv("SUGGESTION_CHANNEL_ID", ""))

# Discord Role IDs
FROGADIER_ROLE_ID = int(os.getenv("FROGADIER_ROLE_ID", ""))
TRADECORD_ROLE_ID = int(os.getenv("TRADECORD_ROLE_ID", ""))
GIVEAWAY_PING_ROLE_ID = int(os.getenv("GIVEAWAY_PING_ROLE_ID", ""))
SWORD_ROLE_ID = int(os.getenv("SWORD_ROLE_ID", ""))
SHIELD_ROLE_ID = int(os.getenv("SHIELD_ROLE_ID", ""))
MALE_ROLE_ID = int(os.getenv("MALE_ROLE_ID", ""))
FEMALE_ROLE_ID = int(os.getenv("FEMALE_ROLE_ID", ""))
OTHER_ROLE_ID = int(os.getenv("OTHER_ROLE_ID", ""))
ORANGE_ROLE_ID = int(os.getenv("ORANGE_ROLE_ID", ""))
YELLOW_ROLE_ID = int(os.getenv("YELLOW_ROLE_ID", ""))
GREEN_ROLE_ID = int(os.getenv("GREEN_ROLE_ID", ""))
BLUE_ROLE_ID = int(os.getenv("BLUE_ROLE_ID", ""))
PURPLE_ROLE_ID = int(os.getenv("PURPLE_ROLE_ID", ""))
BROWN_ROLE_ID = int(os.getenv("BROWN_ROLE_ID", ""))
WHITE_ROLE_ID = int(os.getenv("WHITE_ROLE_ID", ""))
MAROON_ROLE_ID = int(os.getenv("MAROON_ROLE_ID", ""))
MEMBER_ROLE_ID = int(os.getenv("MEMBER_ROLE_ID", ""))
UNASSIGNED_ROLE_ID = int(os.getenv("UNASSIGNED_ROLE_ID", ""))
MUTED_ROLE_ID = int(os.getenv("MUTED_ROLE_ID", ""))
BOT_BAN_ROLE_ID = int(os.getenv("BOT_BAN_ROLE_ID"))

# Discord Message IDs#
RULES_MESSAGE_ID = int(os.getenv("RULES_MESSAGE_ID", ""))

