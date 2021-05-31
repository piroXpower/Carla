from telethon import events
from Evelyn import tbot
from Evelyn.events import Cbot
import Evelyn.modules.sql.chatbot_sql as sql
from requests import get
from . import can_change_info
"""
url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"
"""
@Cbot(pattern="^/chatbot ?(.*)")
async def cb(event):
 if event.is_group:
   if not await can_change_info(event, event.sender_id):
      return
 args = event.pattern_match.group(1)
 if not args:
  mode = sql.chatbot_mode(event.chat_id)
  if mode:
     await event.reply("ChatBot is currently **enabled** for this chat.")
  else:
     await event.reply("ChatBot is currently **disabled** for this chat.")
 elif args in ['on', 'y', 'yes']:
     await event.reply("**Enabled** ChatBot for this chat.")
     sql.set_chatbot_mode(event.chat_id, True)
 elif args in ['off', 'n', 'no']:
     await event.reply("**Disabled** ChatBot for this chat.")
     sql.set_chatbot_mode(event.chat_id, False)
 else:
    await event.reply("Your input was not recognised as one of: yes/no/y/n/on/off")
