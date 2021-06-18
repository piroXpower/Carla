import logging
import os
import sys
import time
from logging import INFO, basicConfig, getLogger

from pyrogram import Client
from telethon import TelegramClient
from telethon.sessions import StringSession

StartTime = time.time()

CMD_LIST = {}
CMD_HELP = {}
LOAD_PLUG = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
LOGGER = logging.getLogger(__name__)
ENV = bool(os.environ.get("ENV", True))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    OWNER_ID = int(os.environ.get("OWNER_ID", 1221693726))
    GBAN_LOGS = os.environ.get("GBAN_LOGS", -100)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)
    DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    API_KEY = os.environ.get("API_KEY", None)
    API_HASH = os.environ.get("API_HASH", None)
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", None)
    DB_URI = os.environ.get("DATABASE_URL", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    WOLFRAM_ID = os.environ.get("WOLFRAM_ID", None)
    LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)
    tbot = TelegramClient(None, API_KEY, API_HASH)
    DEV_USERS = list(DEV_USERS)
    SCREENSHOT_API = os.environ.get("SCREENSHOT_API", None)
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
    IBM_WATSON_CRED_URL = os.environ.get("IBM_WATSON_CRED_URL", None)
    IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", None)
    WALL_API = os.environ.get("WALL_API", None)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    TEMP_MAIL_KEY = os.environ.get("TEMP_MAIL_KEY", None)
    VIRUS_API_KEY = os.environ.get("VIRUS_API_KEY", None)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    UPSTREAM_REPO_URL = os.environ.get(
        "UPSTREAM_REPO_URL", "https://github.com/amarnathcjd/cerina"
    )
    BOT_ID = 1705574750
    sbot = Client("Jessica", bot_token=TOKEN, api_id=API_KEY, api_hash=API_HASH)
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