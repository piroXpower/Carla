from Jessica.modules.sql import afk_sql as sql
from Jessica.events import Cbot
import random

options = [
                "{} is here!",
                "{} is back!",
                "{} is now in the chat!",
                "{} is awake!",
                "{} is back online!",
                "{} is finally here!",
                "Welcome back! {}",
                "Where is {}?\nIn the chat!",
                "Pro {}, is back alive!",
            ]

@Cbot(pattern=r"(.*?)")
async def afk(e):
 if sql.is_afk(sender.id):
   sql.rm_afk(sender.id)
   return await event.reply((random.choice(options)).format(event.sender.first_name))
 for x in [".afk", "/afk", "!afk", "?afk" "brb"]:
  if (event.text.lower()).startswith(x):
    reason = event.text.split(None, 1)[1]
    fname = event.sender.first_name
    user_id = event.sender_id
    sql.set_afk(user_id, reason, fname)
    await event.reply(
           "<b>{}</b> is now AFK !".format(fname),
           parse_mode="html")
