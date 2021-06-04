from sys import exit
from pyrogram import Client

import Evelyn.events  # pylint:disable=E0602
from Evelyn import TOKEN, tbot, API_KEY, API_HASH

try:
    tbot.start(bot_token=TOKEN)
except Exception:
    print("Token Invalid.")
    exit(1)

sbot = Client("wbb", bot_token=TOKEN, api_id=API_KEY, api_hash=API_HASH)

async def start_log():
    await tbot.send_message(-1001273171524, "**Bot Started!**")
sbot.start()

tbot.loop.run_until_complete(start_log())
tbot.run_until_disconnected()
