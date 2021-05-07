from Carla import tbot, OWNER_ID
from . import ELITES, can_change_info, is_admin, is_owner
from Carla.events import Cbot
import os, re
import Carla.modules.sql.blacklist_sql as sql
from telethon import Button, events

@Cbot(pattern="^/addblocklist ?(.*)")
async def _(event):
 if event.is_private:
     return #connect
 if not await can_change_info(event, event.sender_id):
     return
 if event.reply_to_msg_id:
     msg = await event.get_reply_message()
     trigger = msg.message
 elif event.pattern_match.group(1):
     trigger = event.pattern_match.group(1)
 else:
     return await event.reply("You need to provide a blocklist trigger!\neg: `/addblocklist the admins suck`.")
 if len(trigger) > 33:
     return await event.reply("The BlackList filter is too long!")
 text = "Added blocklist filter '{}'!".format(trigger)
 await event.respond(text)
 sql.add_to_blacklist(event.chat_id, trigger)

@Cbot(pattern="^/addblacklist ?(.*)")
async def _(event):
 if event.is_private:
     return #connect
 if not await can_change_info(event, event.sender_id):
     return
 if event.reply_to_msg_id:
     msg = await event.get_reply_message()
     trigger = msg.message
 elif event.pattern_match.group(1):
     trigger = event.pattern_match.group(1)
 else:
     return await event.reply("You need to provide a blocklist trigger!\neg: `/addblocklist the admins suck`.")
 if len(trigger) > 33:
     return await event.reply("The BlackList filter is too long!")
 text = "Added blocklist filter '{}'!".format(trigger)
 await event.respond(text)
 sql.add_to_blacklist(event.chat_id, trigger)
 
@Cbot(pattern="^/(blocklist|blacklist)$")
async def _(event):
 if event.is_private:
     return #connect
 if not await is_admin(event.chat_id, event.sender_id):
     return await event.reply("You need to be an admin to do this.")
 all_blacklisted = sql.get_chat_blacklist(event.chat_id)
 if len(all_blacklisted) == 0:
    text = 'No blocklist filters active in {}!'.format(event.chat.title)
 else:
    text = 'The following blocklist filters are currently active in {}:'.format(event.chat.title)
    for i in all_blacklisted:
          text += f"\n- `{i}`"
 await event.reply(text)

@Cbot(pattern="^/(rmblacklist|rmblocklist) ?(.*)")
async def _(event):
 if event.is_private:
     return #connect
 if not await can_change_info(event, event.sender_id):
     return
 args = event.pattern_match.group(2)
 if not args:
  return await event.reply("You need to specify the blocklist filter to remove")
 d = sql.rm_from_blacklist(event.chat_id, args)
 if d:
   text = "I will no longer blocklist '{}'.".format(args)
 else:
   text = f"`{args}` has not been blocklisted, and so could not be stopped. Use the /blocklist command to see the current blocklist."
 await event.reply(text)

@Cbot(pattern="^/(unblocklistall|unblacklistall)$")
async def _(event):
 if event.is_private:
     return #connect
 if not await is_owner(event, event.sender_id):
     return
 buttons = [Button.inline("Delete blocklist", data="dabl")],[Button.inline("Cancel", data="cabl")]
 text = 'Are you sure you would like to stop **ALL** of the blocklist in {}? This action cannot be undone.'.format(event.chat.title)
 await event.reply(text, buttons=buttons)

@tbot.on(events.CallbackQuery(pattern="dabl"))
async def dabl(event):
  perm = await tbot.get_permissions(event.chat_id, event.sender_id)
  if not perm.is_admin:
    return await event.answer("You need to be an admin.")
  if not perm.is_creator:
    return await event.answer("You need to be the chat creator.")
  await event.edit('Deleted chat blocklist.')
  all_blacklisted = sql.get_chat_blacklist(event.chat_id)
  for i in all_blacklisted:
    try:
     sql.rm_from_blacklist(event.chat_id, i)
    except Exception as e:
     await event.respond(f"{e}")
     
@tbot.on(events.CallbackQuery(pattern="cabl"))
async def cabl(event):
  perm = await tbot.get_permissions(event.chat_id, event.sender_id)
  if not perm.is_admin:
    return await event.answer("You need to be an admin.")
  if not perm.is_creator:
    return await event.answer("You need to be the chat creator.")
  await event.edit("Removal of the blocklist has been cancelled.")
