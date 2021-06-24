from sys import exit

import Jessica.events  # pylint:disable=E0602
from Jessica import TOKEN, tbot

try:
    tbot.start(bot_token=TOKEN)
except Exception:
    print("Token Invalid.")
    exit(1)


tbot.run_until_disconnected()
