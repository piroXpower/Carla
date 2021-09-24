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
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
)


LOGGER = logging.getLogger(__name__)
TOKEN = e.get("TOKEN")
OWNER_ID = 865058466
API_KEY = 3138242
API_HASH = "9ff85074c961b349e6dad943e9b20f54"
DB_URI = "postgres://sqlgzrfkyljzma:6b1a2997b31e0120390f4ff1c208753ed8003f86402ca2bbf27cd256306e533f@ec2-52-19-170-215.eu-west-1.compute.amazonaws.com:5432/d6n5ris8lr007u"
tbot = TelegramClient(None, API_KEY, API_HASH)
STRING_SESSION = "1BVtsOMQBu7EC7pxQ-iHfjwUFpjG4YIUuZ2QqzexjefOKGwS8RSUsyrsU_tR6TMxnAbc6ZAnRkq2KghEYNb0YtQ-v3I5ijU03M-BVYy_w1SslF-5lH2XbF7sSRl5TWa2Jar256brsZvZZNnaEbDTBenTIFBt87hUdLBV5H-O0EeSd96b0a76ULgc91QsRJKZO76GewtsuEP8OrAxKkaP7hPrTAYtXYl7hJTRJ1aKGoWNt5iRr3ViaoeLuEW5PfNutiswKllgub_bDGw9grMLsPHtIaGEeCQrlwXKodWRbTZzhb3ycpabFDzX3bI1DXnGBQ7wI-LDqs37eMHQKDzKgm9fz_L-HFNw="
MONGO_DB_URI = "mongodb+srv://Simpmodz:Simpmodz@rexmodz.d2sxt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
BOT_ID = 1839462992
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
