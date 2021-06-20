import random

from Jessica.events import Cbot
from Jessica.modules.sql import afk_sql as sql

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
    if sql.is_afk(e.sender_id):
        sql.rm_afk(e.sender_id)
        return await e.reply((random.choice(options)).format(e.sender.first_name))
    for x in [".afk", "/afk", "!afk", "?afk" "brb"]:
        if (e.text.lower()).startswith(x):
            try:
                reason = e.text.split(None, 1)[1]
            except IndexError:
                reason = ""
            fname = e.sender.first_name
            user_id = e.sender_id
            sql.set_afk(user_id, reason, fname)
            await e.reply("<b>{}</b> is now AFK !".format(fname), parse_mode="html")
