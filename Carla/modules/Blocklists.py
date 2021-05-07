from Carla import tbot, OWNER_ID
from . import ELITES, can_change_info, is_admin
from Carla.events import Cbot
import os, re
import Carla.modules.sql.blacklist_sql as sql

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
 text = "Added blocklist filter '{}'!".format(trigger)
 sql.add_to_blacklist(event.chat_id, trigger)
 await event.respond(text)
