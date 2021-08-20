from telethon import Button

from .. import OWNER_ID
from ..events import Cbot, Cinline
from . import can_change_info, cb_is_owner, extract_time, can_ban_users
from . import g_time as get_time
from . import get_user, is_owner
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
    c = p = e.pattern_match.group(1)
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
    await e.reply(f"Updated warn mode to:{p}")
    db.set_warn_strength(e.chat_id, c[0], c_time)


@Cbot(pattern="^/setwarntime ?(.*)")
async def set_warn_last__(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await anon_warn()
    if not await can_change_info(e, e.sender_id):
        return
    q = e.pattern_match.group(1)
    if not q:
        return await e.reply("Please specify how long warns should last for.")
    xp = e.text.split(" ", 1)[1]
    time = await extract_time(e, xp)
    await e.reply(
        f"The warn time has been set to {get_time(time)}. Older warns will be automatically removed."
    )
    db.set_warn_expire(e.chat_id, time)


warn_settings = """
There is a {} warning limit in {}. When that limit has been exceeded, the user will be {}.
Warnings {}.
"""


@Cbot(pattern="^/warnings ?(.*)")
async def check_warn___settings__(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await anon_warn()
    if not await can_change_info(e, e.sender_id):
        return
    chat_id = e.chat_id
    title = e.chat.title
    limit, mode, time, expiretime = db.get_warn_settings(chat_id)
    if mode in ["ban", "tban"]:
        d = "banned"
        if mode == "tban":
            d += "for " + str(get_time(time))
    elif mode in ["mute", "tmute"]:
        d = "muted"
        if mode == "tmute":
            d += "for " + str(get_time(time))
    elif mode == "kick":
        d = "kicked"
    if expiretime != 0:
        dc = "expire after{}".format(get_time(expiretime))
    else:
        dc = "do not expire"
    await e.reply(warn_settings.format(limit, title, d, dc))


@Cbot(pattern="^/resetwarn ?(.*)")
async def reset_warns___(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await anon_warn()
    if not await can_change_info(e, e.sender_id):
        return
    user = None
    try:
        user, xtra = await get_user(e)
    except:
        pass
    if user == None:
        return
    reset = db.reset_warns(user.id, e.chat_id)
    if reset:
        await e.reply(
            f"User <a href='tg://user?id={user.id}'>{user.first_name}</a> has had all their previous warns removed.",
            parse_mode="html",
        )
    else:
        await e.reply(
            f"User <a href='tg://user?id={user.id}'>{user.first_name}</a> has no warnings to delete!",
            parse_mode="html",
        )


@Cbot(pattern="^/resetallwarns(@MissNeko_Bot)?$")
async def reset_all_warns_of___chat____(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await anon_warn()
    if not e.sender_id == OWNER_ID and not await is_owner(e, e.sender_id):
        return
    await e.reply(
        f"Are you sure you would like to reset **ALL** warnings in {e.chat.title}? This action cannot be undone.",
        buttons=[
            [Button.inline("Reset all warnings", data="rm_all_w")],
            [Button.inline("Cancel", data="c_rm_all_w")],
        ],
    )


@Cinline(pattern="rm_all_w")
async def rm_all_warns(e):
    if not await cb_is_owner(e, e.sender_id):
        return
    await e.edit("Reset all chat warnings.")
    db.reset_all_warns(e.chat_id)


@Cinline(pattern="c_rm_all_w")
async def c_rm_all_w(e):
    if not await cb_is_owner(e, e.sender_id):
        return
    await e.edit("Resetting of all warnings has been cancelled.")


@Cbot(pattern="^/(warn|swarn|dwarn)(@MissNeko_Bot)? ?(.*)")
async def warn_peepls____(e):
 if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
 if not e.from_id:
        return await anon_warn()
 if not await can_ban_users(e, e.sender_id):
        return
 q = e.text.split(' ', 1)
 if e.reply_to:
   user = (await e.get_reply_message()).sender
   if len(q) == 2:
      reason = q[1]
   else:
       reason = ""
 elif len(q) == 2:
   q = q.split(' ', 1)
   u_obj = q[0]
   if u_obj.isnumeric():
     u_obj = int(u_obj)
   try:
    user = await tbot.get_entity(u_obj)
   except (ValueError, TypeError) as rr:
    return await e.reply(str(rr))
   if len(q) == 2:
     reason = q[1]
   else:
     reason = ''
 await event.reply(str(reason) + str(user.id))
