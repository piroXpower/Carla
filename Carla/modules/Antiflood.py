from Carla import tbot, OWNER_ID
from . import ELITES, can_change_info, extract_time, is_admin
from typing import Optional, List
import re, time
from .sql import antiflood_sql as sql
from telethon import events

badtime = """
It looks like you tried to set time value for antiflood but you didn't specified time; Try, `/setfloodmode [tban/tmute] <timevalue>`.

Examples of time value: `4m = 4 minutes`, `3h = 3 hours`, `6d = 6 days`, `5w = 5` weeks.
"""
badargs = """
I expected some arguments! Either `off`, or an integer. eg: `/setflood 5`, or `/setflood off`
"""

@Cbot(pattern="^/setfloodmode ?(.*)")
async def _(event):
 if event.is_private:
   return #connect
 if not await can_change_info(event, event.sender_id):
   return
 options = event.pattern_match.group(1)
 if not options:
   return await event.reply("You need to specify an action to take upon flooding. Current modes are: ban/kick/mute/tban/tmute")
 supported = ["ban", "mute", "kick", "tban", "tmute"]
 options = options.split()
 if not options[0] in supported:
   return await event.reply(f"Unknown type '{options}'. Please use one of: ban/kick/mute/tban/tmute")
 if options[0] == "ban":
  sql.set_flood_strength(event.chat_id, 1, "0")
  txt = "Banned"
 elif options[0] == "kick":
  sql.set_flood_strength(event.chat_id, 2, "0")
  txt = "Kicked"
 elif options[0] == "mute":
  sql.set_flood_strength(event.chat_id, 3, "0")
  txt = "Muted"
 elif options[0] == "tban":
  if len(options) == 1:
    return await event.reply(badtime)
  time = await extract_time(event, options[1])
  if not time:
    return
  sql.set_flood_strength(event.chat_id, 4, str(time))
  txt = "temporarly Banned for {}".format(options[1])
 elif options[0] == "tmute":
  if len(options) == 1:
    return await event.reply(badtime)
  time = await extract_time(event, options[1])
  if not time:
    return
  sql.set_flood_strength(event.chat_id, 5, str(time))
  txt = "temporarly Muted for {}".format(options[1])
 await event.respond("Updated antiflood reaction in {} to: **{}**".format(event.chat.title, txt))

@Cbot(pattern="^/setflood ?(.*)")
async def _(event):
 if event.text.startswith("/setfloodmode") or event.text.startswith("!setfloodmode") or event.text.startswith("?setfloodmode"):
      return
 if event.is_private:
      return #connect
 if not await can_change_info(event, event.sender_id):
   return
 args = event.pattern_match.group(1)
 if not args:
    return await event.reply(badargs)
 if args == 'off':
    sql.set_flood(event.chat_id, 0)
    text = 'Antiflood has been disabled.'
 elif args == '∞':
    sql.set_flood(event.chat_id, 0)
    text = f"Antiflood settings for {event.chat.title} have been updated to ∞."
 elif args.isdigit():
    if not int(args):
       return await event.reply(f"{args} is not a valid integer.")
    elif int(args) <= 0:
       sql.set_flood(event.chat_id, 0)
       text = 'Antiflood has been disabled.'
    else:
       sql.set_flood(event.chat_id, int(args))
       text = f"Antiflood settings for {event.chat.title} have been updated to {int(args)}."
 else:
   return await event.reply(f'{args}is not a valid integer.')
 await event.respond(text)

@tbot.on(events.NewMessage(pattern=None))
async def flood(event):
 if event.is_private:
      return #connect
 if not event.from_id:
    return
 if event.sender_id in ELITES or event.sender_id == OWNER_ID or await is_admin(event.chat_id, event.sender_id):
      return sql.update_flood(event.chat_id, None)
 should_ban = sql.update_flood(event.chat_id, event.sender_id)
 if not should_ban:
        return
 await event.delete()
 mode, getvalue = sql.get_flood_setting(event.chat_id)
 text = f"Yeah, I don't like yout flooding.\n**{event.sender.first_name}** has been "
 if mode == 1:
   text += "banned."
   await event.respond(text)
   await tbot.edit_permissions(event.chat_id, event.sender_id, view_messages=False)
 elif mode == 2:
   text += "Kicked."
   await event.respond(text)
   await tbot.kick_participant(event.chat_id, event.sender_id)
 elif mode == 3:
   text += "muted."
   await event.respond(text)
   await tbot.edit_permissions(event.chat_id, event.sender_id, send_messages=False)
 elif mode == 4:
   if int(getvalue) < 3600:
     value = int(getvalue)//60
     iid = "{} Minutes".format(value)
   elif int(getvalue) > 3600 < 86400:
     value = int(getvalue)//(60*60)
     iid = "{} Hours".format(value)
   elif int(getvalue) > 86400:
     value = int(getvalue)//(60*60*24)
     iid = "{} Days".format(value)
   text += f"Banned for {iid}."
   await event.respond(text)
   await tbot.edit_permissions(event.chat_id, event.sender_id, until_date=time.time() + int(getvalue), view_messages=False)
 elif mode == 5:
   if int(getvalue) < 3600:
     value = int(getvalue)//60
     iid = "{} Minutes".format(value)
   elif int(getvalue) > 3600 < 86400:
     value = int(getvalue)//(60*60)
     iid = "{} Hours".format(value)
   elif int(getvalue) > 86400:
     value = int(getvalue)//(60*60*24)
     iid = "{} Days".format(value)
   text += f"Muted for {iid}."
   await event.respond(text)
   await tbot.edit_permissions(event.chat_id, event.sender_id, until_date=time.time() + int(getvalue), send_messages=False)

@Cbot(pattern="^/flood")
async def _(event):
 if event.is_private:
   return #connect
 limit = sql.get_flood_limit(event.chat_id)
 if limit == 0:
   text = 'This chat is not currently enforcing flood control.'
 else:
   text = f'This chat is currently enforcing flood control after {limit} messages.'
 await event.respond(text)
