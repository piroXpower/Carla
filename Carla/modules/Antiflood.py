from Carla import tbot, OWNER_ID
from . import ELITES, can_change_info
from typing import Optional, List
import re, time
from .sql import antiflood_sql as sql

@Cbot(pattern="^/setfloodmode ?(.*)")
async def _(event):
 if event.is_private:
   return #connect
 if not can_change_info(event, event.sender_id):
   return
 options = event.pattern_match.group(1)
 if not options:
   return await event.reply("You need to specify an action to take upon flooding. Current modes are: ban/kick/mute/tban/tmute")
 supported = ["ban", "mute", "kick", "tban ?(.*)", "tmute ?(.*)"]
 if not options in supported:
   return await event.reply(f"Unknown type '{options}'. Please use one of: ban/kick/mute/tban/tmute")
 
