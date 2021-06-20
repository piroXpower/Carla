import random

from telethon.tl.types import MessageEntityMention, MessageEntityMentionName

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


@Cbot(pattern=r"(.*?)")
async def afk_check(e):
    if e.is_private:
        return
    if e.reply_to:
        r = await e.get_reply_message()
        user_id = r.sender_id
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
        except Exception:
            return
    if event.sender_id == user_id or not user_id:
        return
    if sql.is_afk(user_id):
        afk = sql.check_afk_status(user_id)
        reason = ""
        if afk.reason:
            reason = "Reason: {afk.reason}"
        await event.reply(
            "<b>{} is AFK !</b>\n\n{}".format(afk.fname, reason), parse_mode="html"
        )
