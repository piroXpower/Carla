import os
import sys

API_KEY = os.environ.get("API_KEY")
API_HASH = os.environ.get("API_HASH")
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
TOKEN = "1842654376:AAHXjoWnlKx_jvazdqJremZ40B0M29ufd2Q"
OWNER_ID = os.environ.get("OWNER_ID")

from telethon import TelegramClient, events

wbot = TelegramClient(None, API_KEY, API_HASH)

try:
    wbot.start(bot_token=TOKEN)
except Exception as e:
    print("Logger Failed to Start." + str(e))
    sys.exit(1)


@wbot.on(events.NewMessage(pattern="^[!.?/]logs$"))
async def logs(event):
    if not event.sender_id == OWNER_ID:
        return
    await event.respond("Logger Test")
