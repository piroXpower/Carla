"""from Evelyn import tbot
from telethon import events
from Evelyn.events import Cbot
import requests

url = "https://alexa-bot-api-web-server.vercel.app/api/alexa?stimulus=${}?lang=$en"

BOT_ID = 1705574750

@tbot.on(events.NewMessage(pattern=None))
async def su(event):
 if event.text.startswith("/") or event.text.startswith(".") or event.text.startswith("?") or event.text.startswith("!"):
   return
 if event.reply_to_msg_id:
   if (await event.get_reply_message()).sender_id != BOT_ID:
      return
 else:
    return
 if event.media:
   return
 text = event.text
 response = requests.request("GET", url.format(text))
 await event.reply(str(response.text))
"""
