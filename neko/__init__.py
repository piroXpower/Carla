import logging
import os
import sys
import time
from logging import INFO, basicConfig, getLogger
from os import environ as e

from telethon import TelegramClient
from telethon.sessions import StringSession

StartTime = time.time()
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

CMD_HELP = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
)


LOGGER = logging.getLogger(__name__)
TOKEN = e.get("TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", 1763477650))
API_KEY = int(os.environ.get("API_KEY", 3138242))
API_HASH = os.environ.get("API_HASH", "9ff85074c961b349e6dad943e9b20f54")
DB_URI = os.environ.get("DATABASE_URL")
tbot = TelegramClient(None, API_KEY, API_HASH)
STRING_SESSION = None
MONGO_DB_URI = os.environ.get(
    "MONGO_DB_URI",
)
BOT_ID = 1839462992
ubot = None
if STRING_SESSION:
    ubot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    ubot = None
try:
    ubot.start()
except:
    print("[INFO]: Failed to start userbot client.")
spam = {}


def spam_check(user_id):
    x = spam.get(user_id)
    if x:
        count, mark = x
        if int(time.time() - mark) < 3:
            count += 1
        if count == 8:
            print(x)
