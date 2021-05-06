from Carla import tbot, OWNER_ID
from . import ELITES, can_change_info, extract_time
from typing import Optional, List
import re, time
from .sql import antiflood_sql as sql

badtime = """
It looks like you tried to set time value for antiflood but you didn't specified time; Try, `/setfloodmode [tban/tmute] <timevalue>`.

Examples of time value: `4m = 4 minutes`, `3h = 3 hours`, `6d = 6 days`, `5w = 5` weeks.
"""

@Cbot(pattern="^/setfloodmode ?(.*)")
async def _(event):
 if event.is_private:
   return #connect
 if not can_change_info(event, event.sender_id):
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
  sql.set_flood_strength(event.chat_id, 4, str(time))
  txt = "Banned for {}".format(options[1])
 elif options[0] == "tmute":
  if len(options) == 1:
    return await event.reply(badtime)
  time = await extract_time(event, options[1])
  sql.set_flood_strength(event.chat_id, 5, str(time))
  txt = "Muted for {}".format(options[1])
 await event.respond("Updated antiflood reaction in {} to: {}.".format(event.chat.title, txt))


