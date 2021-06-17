import time

from telethon import Button, events

from Jessica import tbot
from Jessica.events import Cbot

from . import (
    ELITES,
    can_ban_users,
    cb_can_ban_users,
    extract_time,
    g_time,
    get_user,
    is_admin,
)


async def excecute_operation(
    event, user_id, name, mode, reason="", tt=0, reply_to=None
):
    if name:
        name = ((name).replace("<", "&lt;")).replace(">", "&gt;")
    if event.chat.admin_rights:
        if not event.chat.admin_rights.ban_users:
            return await event.reply("I haven't got the rights to do this.")
    if user_id in ELITES and mode in ["ban", "tban", "mute", "tmute", "kick"]:
        return await event.reply("You can't act against my devs!")
    if mode == "ban":
        await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, view_messages=False
        )
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        else:
            reason = ""
        await event.respond(
            f'Another one bites the dust...! Banned <a href="tg://user?id={user_id}">{name}</a></b>.{reason}',
            parse_mode="html",
            reply_to=reply_to,
        )
    elif mode == "kick":
        await tbot.kick_participant(event.chat_id, int(user_id))
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        else:
            reason = ""
        await event.respond(
            f'I"ve kicked <a href="tg://user?id={user_id}">{name}</a></b>.{reason}',
            parse_mode="html",
            reply_to=reply_to,
        )
    elif mode == "mute":
        await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, send_messages=False
        )
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        else:
            reason = ""
        await event.respond(
            f'Shhh... quiet now.\nMuted <a href="tg://user?id={user_id}">{name}</a>.{reason}',
            parse_mode="html",
            reply_to=reply_to,
        )
    elif mode == "tban":
        final_t = int(tt)
        tt = g_time(tt)
        await event.respond(
            f'Banned <a href="tg://user?id={user_id}">{name}</a> for {tt}!',
            parse_mode="html",
            reply_to=reply_to,
        )
        await tbot.edit_permissions(
            event.chat_id,
            int(user_id),
            until_date=time.time() + final_t,
            view_messages=False,
        )
    elif mode == "tmute":
        final_t = int(tt)
        tt = g_time(tt)
        await event.respond(
            f'Muted <a href="tg://user?id={user_id}">{name}</a> for {tt}!',
            parse_mode="html",
            reply_to=reply_to,
        )
        await tbot.edit_permissions(
            event.chat_id,
            int(user_id),
            until_date=time.time() + final_t,
            send_messages=False,
        )
    elif mode == "unmute":
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        else:
            reason = ""
        unmute = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, send_messages=True
        )
        if unmute:
            await event.respond(
                f'I shall allow <a href="tg://user?id={user_id}">{name}</a></b> to text! {reason}',
                parse_mode="html",
                reply_to=reply_to,
            )
        else:
            await event.reply("This person can already speak freely!")
    elif mode == "unban":
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        else:
            reason = ""
        unban = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, view_messages=True
        )
        if unban:
            await event.respond(f"Fine, they can join again.", reply_to=reply_to)
        else:
            await event.respond(
                "This person hasn't been banned... how am I meant to unban them?",
                reply_to=reply_to,
            )
    elif mode == "sban":
        ban = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, view_messages=False
        )
    elif mode == "smute":
        mute = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, send_messages=False
        )
    elif mode == "skick":
        await tbot.kick_participant(event.chat_id, int(user_id))


@Cbot(pattern="^/dban ?(.*)")
async def dban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        if event.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            if event.chat.admin_rights.delete_messages:
                await reply_msg.delete()
        else:
            return await event.reply(
                "You have to reply to a message to delete it and ban the user."
            )
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "ban"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I unmute an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"dban|{user_id}|0•|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/ban ?(.*)")
async def ban(event):
    if (
        event.text.startswith("!banme")
        or event.text.startswith("/banme")
        or event.text.startswith(".banme")
        or event.text.startswith("?banme")
    ):
        return
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "ban"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"ban|{user_id}|0|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/sban ?(.*)")
async def ban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "sban"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"sban|{user_id}|0|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/unban ?(.*)")
async def unban(event):
    if (
        event.text.startswith(".unbanall")
        or event.text.startswith("?unbanall")
        or event.text.startswith("/unbanall")
        or event.text.startswith("!unbanall")
    ):
        return
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "unban"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I unban an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"unban|{user_id}|0|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/dmute ?(.*)")
async def dban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        if event.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            if event.chat.admin_rights.delete_messages:
                await reply_msg.delete()
        else:
            return await event.reply(
                "You have to reply to a message to delete it and mute the user."
            )
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "mute"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I mute an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"dmute|{user_id}|0•|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/mute ?(.*)")
async def mute(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "mute"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I mute an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"mute|{user_id}|0|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/smute ?(.*)")
async def ban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "smute"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I mute an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"smute|{user_id}|0|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/unmute ?(.*)")
async def unmute(event):
    if (
        event.text.startswith(".unmuteall")
        or event.text.startswith("?unmuteall")
        or event.text.startswith("/unmuteall")
        or event.text.startswith("!unmuteall")
    ):
        return
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "unmute"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I unmute an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"unmute|{user_id}|0•|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/dkick ?(.*)")
async def dban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        if event.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            if event.chat.admin_rights.delete_messages:
                await reply_msg.delete()
        else:
            return await event.reply(
                "You have to reply to a message to delete it and kick the user."
            )
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "kick"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I kick an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"dkick|{user_id}|0•|{event.reply_to_msg_id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/kick ?(.*)")
async def kick(event):
    if (
        event.text.startswith(".kickme")
        or event.text.startswith("/kickme")
        or event.text.startswith("?kickme")
        or event.text.startswith("!kickme")
    ):
        return
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "kick"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I kick an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"kick|{user_id}|0|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/skick ?(.*)")
async def ban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        mode = "skick"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I kick an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            0,
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"skick|{user_id}|0|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/tban ?(.*)")
async def tban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if await is_admin(event.chat_id, user.id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        if not reason:
            return await event.reply(
                "You haven't specified a time to ban this user for!"
            )
        if not reason[0].isdigit():
            return await event.reply(
                "failed to get specified time: {reason} is not a valid number"
            )
        if len(reason) == 1:
            return await event.reply(
                f"""failed to get specified time: '{reason}' does not follow the expected time patterns.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
            )
        tt = await extract_time(event, reason)
        user_id = user.id
        mode = "tban"
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            int(tt),
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if not reason:
            return await event.reply(
                "You haven't specified a time to ban this user for!"
            )
        if not reason[0].isdigit():
            return await event.reply(
                "failed to get specified time: {reason} is not a valid number"
            )
        if len(reason) == 1:
            return await event.reply(
                f"""failed to get specified time: '{reason}' does not follow the expected time patterns.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
            )
        tt = await extract_time(event, reason)
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"tban|{user_id}|{tt}|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/tmute ?(.*)")
async def tban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if event.is_group:
            if not event.sender_id in ELITES:
                if not await can_ban_users(event, event.sender_id):
                    return
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if await is_admin(event.chat_id, user.id):
            return await event.reply(
                "Why would I mute an admin? That sounds like a pretty dumb idea."
            )
        if not reason:
            return await event.reply(
                "You haven't specified a time to ban this user for!"
            )
        if not reason[0].isdigit():
            return await event.reply(
                "failed to get specified time: {reason} is not a valid number"
            )
        if len(reason) == 1:
            return await event.reply(
                f"""failed to get specified time: '{reason}' does not follow the expected time patterns.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
            )
        tt = await extract_time(event, reason)
        user_id = user.id
        mode = "tmute"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(
            event,
            user_id,
            user.first_name,
            mode,
            reason,
            int(tt),
            event.id,
        )
    else:
        reason = ""
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if not reason:
            return await event.reply(
                "You haven't specified a time to mute this user for!"
            )
        if not reason[0].isdigit():
            return await event.reply(
                "failed to get specified time: {reason} is not a valid number"
            )
        if len(reason) == 1:
            return await event.reply(
                f"""failed to get specified time: '{reason}' does not follow the expected time patterns.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
            )
        tt = await extract_time(event, reason)
        user_id = user.id
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"tmute|{user_id}|{tt}|{event.id}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/kickme")
async def k_me(event):
    if not event.is_group:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if await is_admin(event.chat_id, event.sender_id):
        return await event.reply(
            "Ha, I'm not kicking you, you're an admin! You're stuck with everyone here."
        )
    try:
        await tbot.kick_participant(event.chat_id, event.sender_id)
        await event.reply("Yeah, you're right - get out.")
    except:
        await event.reply("Failed to kick!")


@Cbot(pattern="^/banme")
async def ban_me(event):
    if not event.is_group:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if await is_admin(event.chat_id, event.sender_id):
        return await event.reply(
            "Ha, I'm not banning you, you're an admin! You're stuck with everyone here."
        )
    await event.reply("why making a scene just leave bitch!")


@Cbot(pattern="^/rban ?(.*)")
async def rban(event):
    data = event.pattern_match.group(1)
    if not data:
        return


# soon

# Anonymous Admins
# ----------------


@tbot.on(events.CallbackQuery(pattern=r"anonymous(\_(.*))"))
async def anon_admins(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    input = data.split("_", 1)[1]
    input = input.split("|", 3)
    mode = input[0]
    user_id = input[1]
    time = input[2]
    optional_id = int(input[3])
    if not event.sender_id in ELITES:
        if not await cb_can_ban_users(event, event.sender_id):
            return
    ad_check = mode
    if ad_check in ["ban", "sban", "dban"]:
        ad_check = "ban"
    elif ad_check in ["kick", "dkick", "skick"]:
        ad_check = "kick"
    elif ad_check in ["mute", "dmute", "tmute", "dmute"]:
        ad_check = "mute"
    if await is_admin(event.chat_id, int(user_id)):
        return await event.edit(
            f"Why would I {ad_check} an admin? That sounds like a pretty dumb idea."
        )
    if mode in ["dban", "dkick", "dmute"]:
        mode = mode.replace("d", "")
        await tbot.delete_messages(event.chat_id, [optional_id])
    user_obj = await tbot.get_entity(int(user_id))
    first_name = (((user_obj).first_name).replace("<", "&lt;")).replace(
        ">", "&gt;"
    ) or user_obj.first_name
    await cb_excecute_operation(event, user_id, first_name, mode, "", time)


async def cb_excecute_operation(event, user_id, name, mode, reason="", tt=0):
    if event.chat.admin_rights:
        if not event.chat.admin_rights.ban_users:
            return await event.edit("I haven't got the rights to do this.")
    if user_id in ELITES and mode in ["ban", "tban", "mute", "tmute", "kick"]:
        return await event.edit("You can't act against my devs!")
    if mode == "ban":
        await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, view_messages=False
        )
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        else:
            reason = ""
        await event.edit(
            f'Another one bites the dust...! Banned <a href="tg://user?id={user_id}">{name}</a></b>.{reason}',
            parse_mode="html",
        )
    elif mode == "kick":
        await tbot.kick_participant(event.chat_id, int(user_id))
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        else:
            reason = ""
        await event.edit(
            f'I"ve kicked <a href="tg://user?id={user_id}">{name}</a></b>.{reason}',
            parse_mode="html",
        )
    elif mode == "mute":
        await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, send_messages=False
        )
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        else:
            reason = ""
        await event.edit(
            f'<b>Muted <a href="tg://user?id={user_id}">{name}</a></b>!{reason}',
            parse_mode="html",
        )
    elif mode == "tban":
        final_t = int(tt)
        tt = g_time(tt)
        await event.edit(
            f'<b>Banned <a href="tg://user?id={user_id}">{name}</a></b> for {tt}!',
            parse_mode="html",
        )
        await tbot.edit_permissions(
            event.chat_id,
            int(user_id),
            until_date=time.time() + final_t,
            view_messages=False,
        )
    elif mode == "tmute":
        final_t = int(tt)
        tt = g_time(tt)
        await event.edit(
            f'<b>Muted <a href="tg://user?id={user_id}">{name}</a></b> for {tt}!',
            parse_mode="html",
        )
        await tbot.edit_permissions(
            event.chat_id,
            int(user_id),
            until_date=time.time() + final_t,
            send_messages=False,
        )
    elif mode == "unmute":
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        else:
            reason = ""
        unmute = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, send_messages=True
        )
        if unmute:
            await event.edit(
                f'I shall allow <a href="tg://user?id={user_id}">{name}</a></b> to text! {reason}',
                parse_mode="html",
            )
        else:
            await event.edit("This person can already speak freely!")
    elif mode == "unban":
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        else:
            reason = ""
        unban = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, view_messages=True
        )
        if unban:
            await event.edit(f"Fine, they can join again.")
        else:
            await event.edit(
                "This person hasn't been banned... how am I meant to unban them?",
            )
    elif mode == "sban":
        ban = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, view_messages=False
        )
    elif mode == "smute":
        mute = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, send_messages=False
        )
    elif mode == "skick":
        await tbot.kick_participant(event.chat_id, int(user_id))
