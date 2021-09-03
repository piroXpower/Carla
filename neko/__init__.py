import logging
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
CMD_LIST = {}
CMD_HELP = {}
LOAD_PLUG = {}


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
LOGGER = logging.getLogger(__name__)
TOKEN = e.get("TOKEN", None)
OWNER_ID = int(e.get("OWNER_ID", 1221693726))
API_KEY = e.get("API_KEY", None)
API_HASH = e.get("API_HASH", None)
DB_URI = e.get("DATABASE_URL", None)
tbot = TelegramClient(None, API_KEY, API_HASH)
STRING_SESSION = e.get("STRING_SESSION", None)
MONGO_DB_URI = "mongodb://neko:neko1234@iad2-c7-2.mongo.objectrocket.com:52584,iad2-c7-0.mongo.objectrocket.com:52584,iad2-c7-1.mongo.objectrocket.com:52584/neko?replicaSet=25a8afdada8f49d39f2c94edadce9dca"
BOT_ID = int(e.get("BOT_ID"))
ubot = None
if STRING_SESSION:
    ubot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    pass
try:
    ubot.start()
except BaseException:
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
