import random

from telethon.tl.types import MessageEntityMention, MessageEntityMentionName, User
from .mongodb import afk_db as db
import time
from . import get_readable_time
from Jessica import tbot
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
    if not e.sender:
        return
    if db.is_afk(e.sender_id):
        db.unset_afk(e.sender_id)
        return await e.reply((random.choice(options)).format(e.sender.first_name))
    for x in [".afk", "/afk", "!afk", "?afk", "brb"]:
        if (e.text.lower()).startswith(x):
            try:
                reason = e.text.split(None, 1)[1]
            except IndexError:
                reason = ""
            fname = e.sender.first_name
            user_id = e.sender_id
            db.set_afk(user_id, fname, reason)
            await e.reply("<b>{}</b> is now AFK !".format(fname), parse_mode="html")


@Cbot(pattern=r"(.*?)")
async def afk_check(e):
    if e.is_private:
        return
    if not e.from_id:
        return
    user_id = None
    if e.reply_to:
        r = await e.get_reply_message()
        if r:
         if r.sender:
            if isinstance(r.sender, User):
                user_id = r.sender_id
            else:
                return
         else:
            return
    else:
        try:
            for (ent, txt) in e.get_entities_text():
                if ent.offset != 0:
                    break
                if isinstance(ent, MessageEntityMention):
                    pass
                elif isinstance(ent, MessageEntityMentionName):
                    pass
                else:
                    return
                a = txt.split()[0]
                user = await tbot.get_input_entity(a)
                user_id = user.user_id
        except:
            return
    if not user_id:
        return
    if e.sender_id == user_id or not user_id:
        return
    if db.is_afk(user_id):
        afk = db.get_afk(user_id)
        time_seen = get_readable_time(time.time() - int(afk["time"]))
        reason = ""
        if afk["reason"]:
            r_eson = afk["reason"]
            reason = f"Reason: <code>{r_eson}</code>"
        await e.reply(
            "<b>{} is AFK !</b>\nLast Seen: {}\n{}".format(afk["fname"], time_seen, reason), parse_mode="html"
        )
