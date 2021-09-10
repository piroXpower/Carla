import random
import time

from telethon.tl.types import MessageEntityMention, MessageEntityMentionName, User

from .. import CMD_HELP, tbot
from ..utils import Cbot
from . import get_readable_time
from .mongodb import afk_db as db

options = [
    "**{}** is here!, Was afk for {}",
    "**{}** is back!, Been away for {}",
    "**{}** is now in the chat!, Back after {}",
    "**{}** is awake!, Was afk for {}",
    "**{}** is back online!, Been away for {}",
    "**{}** is finally here!, Was afk for {}",
    "Welcome back! **{}**, Was afk for {}",
    "Where is **{}**?\nIn the chat!, Was afk for {}",
    "Pro **{}**, is back alive!, Was afk for {}",
]


@Cbot(pattern=r"(.*?)")
async def afk(e):
    if not e.sender:
        return
    for x in ["+afk", "/afk", "!afk", "?afk", "brb", "i go away"]:
        if (e.text.lower()).startswith(x):
            try:
                reason = e.text.split(None, 1)[1]
            except IndexError:
                reason = ""
            if (e.text.lower()).startswith("i go away"):
                reason = reason.replace("go away", "")
            _x = await e.reply(
                "<b>{}</b> is now AFK !".format(e.sender.first_name), parse_mode="html"
            )
            return db.set_afk(e.sender_id, e.sender.first_name, reason)
    afk = db.get_afk(e.sender_id)
    if afk:
        xp = get_readable_time(time.time() - int(afk.get("time")))
        await e.reply((random.choice(options)).format(e.sender.first_name, xp))
        db.unset_afk(e.sender_id)


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
            "<b>{} is AFK !</b>\nLast Seen: {} ago.\n{}".format(
                x_afk["first_name"], time_seen, reason
            ),
            parse_mode="html",
        )


__name__ = "afk"
__help__ = """
Here is the help for **AFK** module:

- /afk :mark yourself as AFK(away from keyboard).
- brb `<reason>`: same as the afk command - but not a command.
When marked as **AFK**, any mentions will be replied to with a message to say you're not Available!
"""
CMD_HELP.update({__name__: [__name__, __help__]})
