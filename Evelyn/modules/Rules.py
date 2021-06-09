from Evelyn import tbot
import Evelyn.modules.sql.rules_sql as SQL
from Evelyn.events import Cbot

from . import can_change_info
pos = ["on", "yes", "u"]
neg = ["off", "no", "n"]

@Cbot(pattern="^/privaterules ?(.*)")
async def pr(event):
 if event.is_private:
  return
 if not await can_change_info(event, event.sender_id):
    return
 args = event.pattern_match.group(1)
 if not args:
  mode = sql.get_private(event.chat_id):
  if mode:
    await event.reply("Use of /rules will send the rules to the user's PM.")
  else:
    await event.reply(f"All /rules commands will send the rules to {event.chat.title}.")
