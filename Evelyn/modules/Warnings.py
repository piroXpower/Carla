import time

from telethon import Button, events

import Evelyn.modules.sql.warns_sql as sql
from Evelyn import tbot
from Evelyn.events import Cbot, Cinline

from . import (
    can_change_info,
    cb_can_change_info,
    cb_is_owner,
    extract_time,
    g_time,
    get_user,
    is_admin,
    is_owner,
)


@Cbot(pattern="^/setwarnlimit ?(.*)")
async def _(event):
    if event.is_private:
        return  # connect
    if event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
        args = event.pattern_match.group(1)
        if not args:
            await event.reply(
                "Please specify how many warns a user should be allowed to receive before being acted upon."
            )
        elif args.isdigit():
            if int(args) > 20:
                return await event.reply("Max limit is 20.\nTry lowering the limit.")
            sql.set_warn_limit(event.chat_id, args)
            await event.reply(f"Sucessfully updated warn limit to {args}")
        else:
            await event.reply(f"Expected an integer, got '{args}'.")
    else:
        pattern = event.pattern_match.group(1)[:4]
        if not pattern:
            pattern = "None"
        cb_data = str(pattern) + "|" + "setwarnlimit"
        a_text = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        a_button = Button.inline("Click to prove admin", data="anpw_{}".format(cb_data))
        await event.reply(a_text, buttons=a_button)


@Cbot(pattern="^/setwarnmode ?(.*)")
async def _(event):
    if event.is_private:
        return  # connect
    if event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
        args = event.pattern_match.group(1)
        if not args:
            return await event.reply(
                "You need to specify an action to take upon too many warns. Current modes are: ban/kick/mute/tban/tmute"
            )
        arg = args.split()
        if not arg[0] in ["ban", "mute", "kick", "tban", "tmute"]:
            return await event.reply(
                f"Unknown type '{args}'. Please use one of: ban/kick/mute/tban/tmute"
            )
        if arg[0] in ["tban", "tmute"]:
            if len(arg) == 1:
                return await event.reply(
                    "Looks like you're trying to set a temporary value for warnings, but haven't specified a time; use `/setwarnmode tban <timevalue>`.\nExample time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."
                )
            time = await extract_time(event, arg[1])
            sql.set_ban_time(event.chat_id, time)
        await event.reply(f"Updated warn mode to: {args}")
        sql.set_warn_strength(event.chat_id, str(arg[0]))
    else:
        pattern = event.pattern_match.group(1)[:10]
        if not pattern:
            pattern = "None"
        cb_data = str(pattern) + "|" + "setwarnmode"
        a_text = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        a_button = Button.inline("Click to prove admin", data="anpw_{}".format(cb_data))
        await event.reply(a_text, buttons=a_button)


@Cbot(pattern="^/warn ?(.*)")
async def er(event):
    if (
        event.text.startswith("!warns")
        or event.text.startswith("/warns")
        or event.text.startswith("?warns")
        or event.text.startswith(".warns")
        or event.text.startswith(".warnings")
        or event.text.startswith("?warnings")
        or event.text.startswith("!warnings")
        or event.text.startswith("/warnings")
    ):
        return
    if event.is_private:
        return
    if not await can_change_info(event, event.sender_id):
        return
    await warn_user(event)


@Cbot(pattern="^/dwarn ?(.*)")
async def er(event):
    if (
        event.text.startswith("!dwarns")
        or event.text.startswith("/dwarns")
        or event.text.startswith("?dwarns")
    ):
        return
    if event.is_private:
        return
    if not await can_change_info(event, event.sender_id):
        return
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        await msg.delete()
    await warn_user(event)


@Cbot(pattern="^/swarn ?(.*)")
async def swarn(event):
    if event.is_private:
        return
    if not await can_change_info(event, event.sender_id):
        return
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if await is_admin(event.chat_id, int(user)):
        return await event.reply("I'm not going to warn an admin!")
    limit = sql.get_limit(event.chat_id)
    num_warns, reasons = sql.warn_user(user.id, event.chat_id, reason)
    if num_warns >= limit:
        tt = 0
        mode = sql.get_warn_strength(event.chat_id)
        if mode in ["tban", "tmute"]:
            tt = sql.get_ban_time(event.chat_id)
        sql.reset_warns(user.id, event.chat_id)
        await excecute_warn(event, user.id, user.first_name, mode, reason, tt, limit)


async def warn_user(event):
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if extra:
        reason = f"\n<b>Reason:</b> {extra}"
    else:
        reason = ""
    if await is_admin(event.chat_id, user.id):
        return await event.reply("I'm not going to warn an admin!")
    limit = sql.get_limit(event.chat_id)
    num_warns, reasons = sql.warn_user(user.id, event.chat_id, reason)
    if num_warns < limit:
        text = f'User <a href="tg://user?id={user.id}">{user.first_name}</a> has {num_warns}/{limit} warnings; be careful!.{reason}'
        buttons = [Button.inline("Remove warn (admin only)", data=f"rm_warn-{user.id}")]
        await event.respond(
            text,
            buttons=buttons,
            parse_mode="html",
            reply_to=event.reply_to_msg_id or event.id,
        )
    else:
        tt = 0
        mode = sql.get_warn_strength(event.chat_id)
        if mode in ["tban", "tmute"]:
            tt = sql.get_ban_time(event.chat_id)
        sql.reset_warns(user.id, event.chat_id)
        await excecute_warn(event, user.id, user.first_name, mode, reason, tt, limit)


async def excecute_warn(event, user_id, name, mode, reason="", tt=0, limit=3):
    if mode == "ban":
        await tbot.edit_permissions(
            event.chat_id, user_id, until_date=None, view_messages=False
        )
        if reason:
            reason = f"\nReason: <i>{reason}</i>"
        await event.respond(
            f'Thats <b>{limit}/{limit}</b> Warnings, <a href="tg://user?id={user_id}">{name}</a> Has been <b>Banned!</b>{reason}',
            parse_mode="html",
            reply_to=event.reply_to_msg_id or event.id,
        )
    elif mode == "kick":
        await tbot.kick_participant(event.chat_id, event.sender_id)
        if reason:
            reason = f"\nReason: <i>{reason}</i>"
        await event.respond(
            f'Thats <b>{limit}/{limit}</b> Warnings, <a href="tg://user?id={user_id}">{name}</a> has been <b>Kicked!</b>{reason}',
            parse_mode="html",
            reply_to=event.reply_to_msg_id or event.id,
        )
    elif mode == "mute":
        await tbot.edit_permissions(
            event.chat_id, event.sender_id, until_date=None, send_messages=False
        )
        if reason:
            reason = f"\nReason: <i>{reason}</i>"
        await event.respond(
            f'Thats <b>{limit}/{limit}</b> Warnings, <a href="tg://user?id={user_id}">{name}</a> has been <b>Muted!</b>{reason}',
            parse_mode="html",
            reply_to=event.reply_to_msg_id or event.id,
        )
    elif mode == "tban":
        if reason:
            reason = f"\nReason: <i>{reason}</i>"
        f_t = g_time(tt)
        await event.respond(
            f'Thats <b>{limit}/{limit}</b> Warnings, <a href="tg://user?id={user_id}">{name}</a> has been Banned for <b>{f_t}</b>!{reason}',
            parse_mode="html",
            reply_to=event.reply_to_msg_id or event.id,
        )
        await tbot.edit_permissions(
            event.chat_id,
            event.sender_id,
            until_date=time.time() + int(tt),
            view_messages=False,
        )
    elif mode == "tmute":
        if reason:
            reason = f"\nReason: <i>{reason}</i>"
        f_t = g_time(tt)
        await event.respond(
            f'Thats <b>{limit}/{limit}</b> Warnings, <a href="tg://user?id={user_id}">{name}</a> has been Muted for <b>{f_t}</b>!{reason}',
            parse_mode="html",
            reply_to=event.reply_to_msg_id or event.id,
        )
        await tbot.edit_permissions(
            event.chat_id,
            event.sender_id,
            until_date=time.time() + int(tt),
            send_messages=False,
        )


@tbot.on(events.CallbackQuery(pattern=r"rm_warn-(\d+)"))
async def rm_warn(event):
    user_id = int(event.pattern_match.group(1))
    perm = await tbot.get_permissions(event.chat_id, event.sender_id)
    if not perm.is_admin:
        return await event.answer("You need to be an admin to do this.")
    if not perm.ban_users:
        return await event.edit(
            "You are missing the following rights to use this command: CanBanUsers."
        )
    await event.edit(
        f'<b>Warn</b> removed by <a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a>.',
        parse_mode="html",
    )
    sql.remove_warn(user_id, event.chat_id)


@Cbot(pattern="^/rmwarn ?(.*)")
async def le(event):
    if event.is_private:
        return
    if not await can_change_info(event, event.sender_id):
        return
    user = None
    reason = ""
    try:
        user, reason = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if reason:
        reason = "\n<b>Reason:</b> {reason}"
    result = sql.get_warns(user.id, event.chat_id)
    if result and result[0] in [0, False]:
        return await event.reply(
            "User <a href='tg://user?id={user_id}'>{first_name}</a> has no Warnings.",
            parse_mode="htm",
        )
    user_id = user.id
    chat_id = event.chat_id
    first_name = user.first_name
    text = f"Removed <a href='tg://user?id={user_id}'>{first_name}</a>'s last warn.{reason}"
    await event.reply(text, parse_mode="htm")
    sql.remove_warn(user_id, chat_id)


@Cbot(pattern="^/resetwarn ?(.*)")
async def reset_warn(event):
    if event.is_private:
        return
    if not await can_change_info(event, event.sender_id):
        return
    user = None
    reason = ""
    try:
        user, reason = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if reason:
        reason = "\n<b>Reason:</b> {reason}"
    result = sql.get_warns(user.id, event.chat_id)
    if result and result[0] in [0, False]:
        return await event.reply(
            f"User <a href='tg://user?id={user.id}'>{user.first_name}</a> has no warnings to delete!",
            parse_mode="html",
        )
    await event.reply(
        f"User <a href='tg://user?id={user.id}'>{user.first_name}</a> has had all their previous warns removed.",
        parse_mode="html",
    )
    sql.reset_warns(user.id, event.chat_id)


chat_warns = """
There is a {} warning limit in {}. When that limit has been exceeded, the user will be {}.
Warnings do not expire.
"""


@Cbot(pattern="^/warnings$")
async def warns(event):
    if event.is_private:
        return
    if event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    limit = sql.get_limit(event.chat_id)
    chat_title = event.chat.title
    warn_mode = sql.get_warn_strength(event.chat_id)
    if warn_mode in ["tban", "tmute"]:
        tt = sql.get_ban_time(event.chat_id)
        tt = g_time(tt)
        if warn_mode == "tban":
            warn_mode = f"Banned for {tt}"
        else:
            warn_mode = f"Muted for {tt}"
    elif warn_mode == "ban":
        warn_mode = "Banned"
    elif warn_mode == "kick":
        warn_mode = "Kicked"
    elif warn_mode == "mute":
        warn_mode = "Muted"
    final_str = chat_warns.format(limit, chat_title, warn_mode)
    await event.reply(final_str)


@Cbot(pattern="^/resetallwarns")
async def reset_all_w(event):
    if event.is_private:
        return
    if event.from_id:
        if not await is_owner(event, event.sender_id):
            return
        c_text = f"Are you sure you would like to reset **ALL** warnings in {event.chat.title}? This action cannot be undone."
        buttons = [
            [Button.inline("Reset all warnings", data="rm_all_w")],
            [Button.inline("Cancel", data="c_rm_all_w")],
        ]
        await event.reply(c_text, buttons=buttons)
    else:
        pattern = "None"
        cb_data = str(pattern) + "|" + "resetallwarns"
        a_text = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        a_button = Button.inline("Click to prove admin", data="anpw_{}".format(cb_data))
        await event.reply(a_text, buttons=a_button)


@Cinline(pattern="rm_all_w")
async def rm_all_w(event):
    if not await cb_is_owner(event, event.sender_id):
        return
    await event.edit("Reset all chat warnings.")
    sql.reset_all_warns(event.chat_id)


@Cinline(pattern="c_rm_all_w")
async def c_rm_all_w(event):
    if not await cb_is_owner(event, event.sender_id):
        return
    await event.edit("Resetting of all warnings has been cancelled.")


# Anonymous Admins
@tbot.on(events.CallbackQuery(pattern=r"anpw(\_(.*))"))
async def _(event):
    if not await cb_can_change_info(event, event.sender_id):
        return
    tata = event.pattern_match.group(1)
    data = tata.decode()
    input = data.split("|", 1)[1]
    pattern, mode = input.split("_", 1)
    pattern = pattern.strip()
    mode = mode.strip()
    if pattern == "None":
        pattern = None
    await event.edit(str(mode) + "\n" + str(pattern))
