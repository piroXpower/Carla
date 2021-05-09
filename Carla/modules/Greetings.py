from Carla import tbot, OWNER_ID
from . import can_change_info, ELITES
from Carla.events import Cbot
import Carla.modules.sql.welcome_sql as sql
import Carla.modules.sql.captcha_sql as cas
from telethon import events, Button

wlc_st = """
I am currently welcoming users: `{}`
I am currently deleting old welcomes: `{}`
I am currently deleting service messages: `True`
CAPTCHAs are `{}`.
"""
pos = ['yes', 'y', 'on']
neg = ['n', 'no', 'off']

@Cbot(pattern="^/welcome ?(.*)")
async def _(event):
 if event.is_private:
   return
 if not await can_change_info(event, event.sender_id):
   return
 args = event.pattern_match.group(1)
 if not args:
  bstr = 'False'
  welc = str(sql.is_chat(event.chat_id))
  cws = sql.get_current_welcome_settings(event.chat_id)
  if cws:
   if cws.should_clean_welcome is True:
    bstr = 'True'
  mode = str(cas.get_mode(event.chat_id))
  await event.reply(wlc_st.format(welc, bstr, mode))
 elif args in pos:
  await event.reply("I'll be welcoming all new members from now on!")
  sql.add_c(event.chat_id)
 elif args in neg:
  await event.reply("I'll stay quiet when new members join.")
  sql.rmc(event.chat_id)
 else:
  await event.reply("Your input was not recognised as one of: yes/no/on/off")

@tbot.on(events.ChatAction())
async def _(event):
 if not user.joined:
  return
 if not sql.is_chat(event.chat_id):
  return
 if cas.get_mode(event.chat_id) == True:
  return
 cws = sql.get_current_welcome_settings(event.chat_id)
 if not cws:
  await event.reply(f"Hey {event.sender.first_name}, Welcome to {event.chat.title}! How are you?")

