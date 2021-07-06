import random
import time

from telethon.tl.types import MessageEntityMention, MessageEntityMentionName, User

from Jessica import tbot
from Jessica.events import Cbot

from . import get_readable_time
from .mongodb import afk_db as db

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
    for x in [".afk", "/afk", "!afk", "?afk", "brb"]:
        if (e.text.lower()).startswith(x):
            try:
                reason = e.text.split(None, 1)[1]
            except IndexError:
                reason = ""
            await e.reply(
                "<b>{}</b> is now AFK !".format(e.sender.first_name), parse_mode="html"
            )
            return db.set_afk(e.sender_id, e.sender.first_name, reason)
    if db.is_afk(e.sender_id):
        await e.reply((random.choice(options)).format(e.sender.first_name))
        return db.unset_afk(e.sender_id)


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
    x_afk = db.get_afk(user_id)
    if x_afk:
        time_seen = get_readable_time(time.time() - int(x_afk["time"]))
        reason = ""
        if x_afk["reason"]:
            r_eson = x_afk["reason"]
            reason = f"Reason: <code>{r_eson}</code>"
        await e.reply(
            "<b>{} is AFK !</b>\nLast Seen: <code>{}</code> ago.\n{}".format(
                x_afk["first_name"], time_seen, reason
            ),
            parse_mode="html",
        )
