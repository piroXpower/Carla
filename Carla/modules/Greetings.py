from Carla import tbot, OWNER_ID
from . import can_change_info, ELITES
import re
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

@Cbot(pattern="^/setwelcome ?(.*)")
async def _(event):
 if event.is_private:
    return
 if not await can_change_info(event, event.sender_id):
    return
 if not event.reply_to_msg_id and not event.pattern_match.group(1):
    return await event.reply("You need to give the welcome message some content!")
 elif event.reply_to_msg_id:
   msg = await event.get_reply_message()
   cws = sql.get_current_welcome_settings(event.chat_id)
   if cws:
     sql.rm_welcome_setting(event.chat_id)
   if msg.media:
     tbot_api_file_id = pack_bot_file_id(msg.media)
     sql.add_welcome_setting(event.chat_id, msg.message, False, 0, tbot_api_file_id)
   else:
     sql.add_welcome_setting(event.chat_id, msg.message, False, 0, None)
 elif event.pattern_match.group(1):
   cws = sql.get_current_welcome_settings(event.chat_id)
   if cws:
     sql.rm_welcome_setting(event.chat_id)
   input_str = event.text.split(None, 1)
   sql.add_welcome_setting(event.chat_id, input_str[1], False, 0, None)
 await event.reply("The new welcome message has been saved!")

@tbot.on(events.ChatAction())
async def ca(event):
 if not event.user_joined:
    return
 
