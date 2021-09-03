from sys import exit

import neko.utils  # pylint:disable=E0602
from neko import TOKEN, tbot

try:
    tbot.start(bot_token=TOKEN)
except Exception:
    print("Token Invalid.")
    exit(1)


tbot.run_until_disconnected()
