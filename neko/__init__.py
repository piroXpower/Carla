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

CMD_HELP = {}

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
except:
    print("[INFO]: Failed to start userbot client.")
HU = "BQCZNZgAIqTJH0YPSUI8_c2HmtDch7_bunnamkVEIxJwVsA9tSkVJymu7Y1VBuDuRdGX5E9ZNsFcd17oO3sa_VcyQfQUv72iHO4Fq7EjCGoQM5gLSzYrPprlwR2QJsA4Bd9gVrvDPASKjx-70Ne_ltnx9Qv3XgnM6G7yZWJj6KjU3WvwbHXjQQXy4q4gxdtnxt618bu1qCChv0DkrsVd1PDCoQkd3Os8-CoVjAkn_JNhcG3Z1Ccbebu3elZm7ipbwAePiZAIOzZVyF0A4Nsuo0VywKjrpwOtYeeuiTgf2DlsWD5NgZ2j1IC3eLb0RDjO8W6OXCT2bupIag-n6XBccuP-Z_NPWQA"
spam = {}


def spam_check(user_id):
    x = spam.get(user_id)
    if x:
        count, mark = x
        if int(time.time() - mark) < 3:
            count += 1
        if count == 8:
            print(x)
