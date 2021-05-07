from Carla import tbot, OWNER_ID
from . import ELITES, can_change_info, is_admin
from Carla.events import Cbot
import os, re
import .sql.blacklist_sql as sql

@Cbot(pattern="^/addblocklist ?(.*)")
async def _(event):
 if event.is_private:
     return #connect
 if not await can_change_info(event, event.sendet_id):
     return
 if event.reply_to_msg_id:
     msg = await event.get_reply_message()
     trigger = msg.message
     print(7)
