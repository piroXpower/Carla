from ..events import Cbot
from . import can_change_info, extract_time
from .mongodb import warns_db as db


@Cbot(pattern="/setwarnlimit ?(.*)")
async def set_warn_limit____(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await anon_warn()
    if not await can_change_info(e, e.sender_id):
        return
    c = e.pattern_match.group(1)
    if not c:
        await e.reply(
            "Please specify how many warns a user should be allowed to receive before being acted upon."
        )
    elif c.isdigit():
        if int(c) > 128:
            return await e.reply("Max no of warn limit is 128!")
        await e.reply(
            "Warn limit settings for {} have been updated to {}.".format(
                e.chat.title, c
            )
        )
        db.set_warn_limit(e.chat_id, int(c))
    else:
        await e.reply(f"Expected an integer, got '{c}'.")


@Cbot(pattern="/setwarnmode ?(.*)")
async def set_warn__mode____(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await anon_warn()
    if not await can_change_info(e, e.sender_id):
        return
    c = e.pattern_match.group(1)
    if not c:
        return await e.reply(
            "You need to specify an action to take upon too many warns. Current modes are: ban/kick/mute/tban/tmute"
        )
    c = c.split(None, 1)
    if not c[0] in ["ban", "kick", "mute", "tban", "tmute"]:
        return await e.reply(
            f"Unknown type '{c[0]}'. Please use one of: ban/kick/mute/tban/tmute"
        )
    c_time = 0
    if c[0] in ["tban", "tmute"]:
        try:
            c_time = await extract_time(e, c[1])
        except IndexError:
            return await e.reply(
                "Looks like you're trying to set a temporary value for warnings, but haven't specified a time; use `/setwarnmode tban <timevalue>`.\nExample time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."
            )
    await e.reply(f"Updated warn mode to:{c}")
    db.set_warn_strength(e.chat_id, c[0], c_time)
