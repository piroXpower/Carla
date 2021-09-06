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
cdb = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
LOGGER = logging.getLogger(__name__)
TOKEN = e.get("TOKEN")
OWNER_ID = 1763477650
API_KEY = 4529547
API_HASH = "55bc2f0ca39d588ce5471e52acbf5a69"
DB_URI = "postgres://sqlgzrfkyljzma:6b1a2997b31e0120390f4ff1c208753ed8003f86402ca2bbf27cd256306e533f@ec2-52-19-170-215.eu-west-1.compute.amazonaws.com:5432/d6n5ris8lr007u"
tbot = TelegramClient(None, API_KEY, API_HASH)
STRING_SESSION = "1BVtsOLcBu2LNzWa2posqI-o76Mkf9NPsETLJ_mwRI2pBb3CZSYSdZocRZwYviKplOhdRzTleBMKJr36rfjif4C8p6lklxJYhcz2zmDN2AieU0Jhjqc0XZirv3QfxbDIxPxWaRYioVRdz9WSoy1j_Szfym-elQ1w_BnAsLE5cvU4rNoK21y7eoqTduFvwYxttFhEHH4p0uXNakcjs_AKhgLP3uWM3yKFP0gEzK57LY65GiJn4xzrGFg-8rO3lW2DcmbqStfYSKViKftyzp7-GMHq16OLLPim0jV0d7_hAcpb0onR87nh_25tSDATdPNNPHmweRJd4PA5xa7JsLzT53dlbQ4ScCaE="
MONGO_DB_URI = "mongodb://neko:neko1234@iad2-c7-2.mongo.objectrocket.com:52584,iad2-c7-0.mongo.objectrocket.com:52584,iad2-c7-1.mongo.objectrocket.com:52584/neko?replicaSet=25a8afdada8f49d39f2c94edadce9dca"
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
