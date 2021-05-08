from Carla import tbot, BOT_ID, OWNER_ID
import Carla.modules.sql.warns_sql as sql
from Carla.events import Cbot
from telethon import Button, events
from . import can_change_info, ELITES, is_admin

@Cbot(pattern="^/warnlimit ?(.*)")
async def _(event):
 if event.is_private:
  return #connect
 if not await can_change_info(event, event.sender_id):
  return 
 args = event.pattern_match.group(1)
 if not args:
  settings = sql.get_limit(event.chat_id)
  await event.reply(f"Current warn limit is {settings}\n\nTo change this send the command with the new limit.")
 
