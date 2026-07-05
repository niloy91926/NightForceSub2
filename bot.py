import logging
from telethon import TelegramClient, events, Button
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from decouple import config
from telethon.utils import get_display_name

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ForceSubBot")

# ===== CONFIG =====
BOT_TOKEN = config("BOT_TOKEN")
API_ID = config("API_ID", cast=int)
API_HASH = config("API_HASH")

CHANNELS = config("CHANNELS").split()

WELCOME_MSG = config("WELCOME_MSG", default="Welcome {mention}")
WELCOME_NOT_JOINED = config("WELCOME_NOT_JOINED", default="Join all channels first!")

ON_JOIN = config("ON_JOIN", cast=bool, default=True)
ON_NEW_MSG = config("ON_NEW_MSG", cast=bool, default=True)

# ===== CLIENT =====
bot = TelegramClient("ForceSubBot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

log.info("Bot started...")
