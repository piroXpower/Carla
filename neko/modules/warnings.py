import time

from telethon import Button, types

from .. import OWNER_ID
from ..utils import Cbot, Cinline
from . import (
    can_ban_users,
    can_change_info,
    cb_can_ban_users,
    cb_is_owner,
    extract_time,
)
from . import g_time as get_time
from . import get_user, is_admin, is_owner
from .mongodb import warns_db as db


@Cbot(pattern="^/setwarnlimit ?(.*)")
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


@Cbot(pattern="^/setwarnmode ?(.*)")
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


@Cbot(pattern="^/resetallwarns(@DecodeManagerBot)?$")
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


@Cbot(pattern="^/(warn|swarn|dwarn)(@DecodeManagerBot|DecodeManagerBot)? ?(.*)")
async def warn_peepls____(e):
    for x in [
        "+warnings",
        "/warnings",
        "!warnings",
        "?warnings",
        "+warns",
        "/warns",
        "!warns",
        "?warns",
    ]:
        if e.text.startswith(x):
            return
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await anon_warn()
    if not await can_ban_users(e, e.sender_id):
        return
    q = e.text.split(" ", 1)
    pq = q[0]
    for x in ["+", "?", "/", "!"]:
        pq = pq.replace(x, "")
    if e.reply_to:
        user = (await e.get_reply_message()).sender
        if len(q) == 2:
            reason = q[1]
        else:
            reason = ""
    elif len(q) == 2:
        q = q[1].split(" ", 1)
        u_obj = q[0]
        if u_obj.isnumeric():
            u_obj = int(u_obj)
        try:
            user = await e.client.get_entity(u_obj)
        except (ValueError, TypeError) as rr:
            return await e.reply(str(rr))
        if len(q) == 2:
            reason = q[1]
        else:
            reason = ""
    else:
        return await e.reply("I can't warn nothing! Tell me to whom I should warn!")
    if not user or isinstance(user, types.Channel):
        return await e.reply("I can't warn nothing! Tell me to whom I should warn!")
    if await is_admin(e.chat_id, user.id):
        return await e.reply("Well.. you are wrong. You can't warn an admin.")
    if pq == "dwarn":
        await (await e.get_reply_message()).delete()
    warn, strength, actiontime, limit, num_warns, reasons = db.warn_user(
        user.id, e.chat_id, reason
    )
    if reason:
        reason = f"\n<b>Reason:</b>\n{reason}"
    if not warn:
        text = f'User <a href="tg://user?id={user.id}">{user.first_name}</a> has {num_warns}/{limit} warnings; be careful!{reason}'
        buttons = [
            Button.inline("Remove warn (Admin Only)", data="rmwarn_{}".format(user.id))
        ]
        if not pq == "swarn":
            await e.respond(
                text,
                buttons=buttons,
                parse_mode="html",
                reply_to=e.reply_to_msg_id or e.id,
            )
    else:
        if strength == "tban":
            await tbot.edit_permissions(
                e.chat_id,
                user.id,
                until_date=time.time() + int(actiontime),
                view_messages=False,
            )
            action = "banned for" + get_time(actiontime)
        elif strength == "tmute":
            await tbot.edit_permissions(
                e.chat_id,
                user.id,
                until_date=time.time() + int(actiontime),
                send_messages=False,
            )
            action = "muted for" + get_time(actiontime)
        elif strength == "ban":
            await tbot.edit_permissions(e.chat_id, user.id, view_messages=False)
            action = "banned"
        elif strength == "mute":
            await tbot.edit_permissions(e.chat_id, user.id, send_messages=False)
            action = "muted"
        elif strength == "kick":
            await tbot.kick_participant(e.chat_id, user.id)
            action = "kicked"
        warn_action_notif = (
            "That's {}/{} warnings; <a href='tg://user?id={}'>{}</a> is {}!".format(
                num_warns, limit, user.id, user.first_name, action
            )
        )
        qp = 0
        if reasons:
            rr = "\n<b>Reasons:</b>"
            for reason in reasons:
                qp += 1
                rr += "\n{}: {}".format(qp, reason)
            warn_action_notif += rr
        await e.respond(
            warn_action_notif, reply_to=e.reply_to_msg_id or e.id, parse_mode="html"
        )


@Cbot(pattern="^/warns(@DeCodeManagerBot)? ?(.*)")
async def warns___(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await anon_warn()
    q = e.text.split(" ", 1)
    if e.reply_to:
        user = (await e.get_reply_message()).sender
    elif len(q) == 2:
        q = q[1].split(" ", 1)
        u_obj = q[0]
        if u_obj.isnumeric():
            u_obj = int(u_obj)
        try:
            user = await e.client.get_entity(u_obj)
        except (ValueError, TypeError) as rr:
            return await e.reply(str(rr))
    else:
        user = e.sender
    warns = db.get_warns(user.id, e.chat_id)
    if not warns or warns[0] == 0:
        await e.reply(
            f"User <a href='tg://user?id={user.id}'>{user.first_name}</a> has no warnings!",
            parse_mode="html",
        )
    else:
        count, reasons = warns
        limit = db.get_warn_limit(e.chat_id)
        r = "User <a href='tg://user?id={}'>{}</a> has {}/{} warnings."
        if reasons:
            r += "\nReasons are:"
            qc = 0
            for x in reasons:
                qc += 1
                r += "\n{}. {}".format(qc, x)
        await e.reply(
            r.format(user.id, user.first_name, count, limit), parse_mode="html"
        )


@Cbot(pattern="^/rmwarn(@DeCodeManagerBot)? ?(.*)")
async def rmwarns__(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await anon_warn()
    if not await can_ban_users(e, e.sender_id):
        return
    q = e.text.split(" ", 1)
    if e.reply_to:
        user = (await e.get_reply_message()).sender
        if len(q) == 2:
            reason = q[1]
        else:
            reason = ""
    elif len(q) == 2:
        q = q[1].split(" ", 1)
        u_obj = q[0]
        if u_obj.isnumeric():
            u_obj = int(u_obj)
        try:
            user = await e.client.get_entity(u_obj)
        except (ValueError, TypeError) as rr:
            return await e.reply(str(rr))
        if len(q) == 2:
            reason = q[1]
        else:
            reason = ""
    else:
        return await e.reply(
            "I can't remove warns of nothing! Tell me user whose warn should be removed!"
        )
    rm = db.remove_warn(user.id, e.chat_id)
    if rm:
        if reason:
            reason = "\nReason: {reason}"
        await e.reply(
            "Removed <a href='tg://user?id={}'>{}</a>'s last warn.{}".format(
                user.id, user.first_name, reason
            ),
            parse_mode="html",
        )
    else:
        await e.reply(
            "User <a href='tg://user?id={}'>{}</a> has no Warnings.".format(
                user.id, user.first_name
            ),
            parse_mode="htm",
        )


@Cinline(pattern=r"rmwarn(\_(.*))")
async def rm_warn_cb(e):
    if not await cb_can_ban_users(e, e.sender_id):
        return
    r = e.pattern_match.group(1).decode().split("_", 1)[1]
    r = int(r)
    await e.edit(
        "Warn removed by Admin <a href='tg://user?id={}'>{}</a>".format(
            e.sender_id, e.sender.first_name
        ),
        parse_mode="html",
    )
    db.remove_warn(r, e.chat_id)
