from sys import argv, exit
from Elsie import tbot
from Elsie import TOKEN

import Elsie.events

try:
    tbot.start(bot_token=TOKEN)
except Exception:
    print("Token Invalid.")
    exit(1)

async def start_log():
 await tbot.send_message(-1001273171524, "**Bot Started!**")

tbot.loop.run_until_complete(start_log())
tbot.run_until_disconnected()
