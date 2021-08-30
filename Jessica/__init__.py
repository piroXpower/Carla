import logging
import os
import sys
import time
from logging import INFO, basicConfig, getLogger

from telethon import TelegramClient
from telethon.sessions import StringSession

StartTime = time.time()

CMD_LIST = {}
CMD_HELP = {}
LOAD_PLUG = {}
spam_db = {}
spam = []

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
LOGGER = logging.getLogger(__name__)
ENV = bool(os.environ.get("ENV", True))

if ENV:
    MAINTENANCE = os.environ.get("MAINTENANCE", False)
    TOKEN = os.environ.get("TOKEN", None)
    OWNER_ID = int(os.environ.get("OWNER_ID", 1221693726))
    GBAN_LOGS = os.environ.get("GBAN_LOGS", -100)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)
    API_KEY = os.environ.get("API_KEY", None)
    API_HASH = os.environ.get("API_HASH", None)
    DB_URI = os.environ.get("DATABASE_URL", None)
    WOLFRAM_ID = os.environ.get("WOLFRAM_ID", None)
    tbot = TelegramClient(None, API_KEY, API_HASH)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    MONGO_DB_URI = "mongodb://neko:neko1234@iad2-c7-2.mongo.objectrocket.com:52584,iad2-c7-0.mongo.objectrocket.com:52584,iad2-c7-1.mongo.objectrocket.com:52584/neko?replicaSet=25a8afdada8f49d39f2c94edadce9dca"
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    UPSTREAM_REPO_URL = os.environ.get(
        "UPSTREAM_REPO_URL", "https://github.com/amarnathcjd/cerina"
    )
    BOT_ID = int(os.environ.get("BOT_ID"))
    if MAINTENANCE == "True":
        print("Maintenance Mode Active.")
        sys.exit(0)
    if STRING_SESSION:
        ubot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
    else:
        pass
    try:
        ubot.start()
    except BaseException:
        print("Invalid STRING SESSION!")
else:
    sys.exit(1)
