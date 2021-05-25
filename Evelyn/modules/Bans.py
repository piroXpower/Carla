import time

from telethon import Button, events

from Evelyn import tbot
from Evelyn.events import Cbot

from . import (
    ELITES,
    can_ban_users,
    cb_can_ban_users,
    extract_time,
    g_time,
    get_user,
    is_admin,
)


async def excecute_operation(event, user_id, name, mode, reason="", tt=0):
    if mode == "ban":
        await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, view_messages=False
        )
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        await event.respond(
            f'Another one bites the dust...! Banned <a href="tg://user?id={user_id}">{name}</a></b>.{reason}',
            parse_mode="html",
        )
    elif mode == "kick":
        await tbot.kick_participant(event.chat_id, int(user_id))
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        await event.respond(
            f'I"ve kicked <a href="tg://user?id={user_id}">{name}</a></b>.{reason}',
            parse_mode="html",
        )
    elif mode == "mute":
        await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, send_messages=False
        )
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        await event.respond(
            f'<b>Muted <a href="tg://user?id={user_id}">{name}</a></b>!{reason}',
            parse_mode="html",
        )
    elif mode == "tban":
        final_t = int(tt)
        tt = g_time(tt)
        await event.respond(
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
        await event.respond(
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
        unmute = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, send_messages=True
        )
        if unmute:
            await event.respond(
                f'I shall allow <a href="tg://user?id={user_id}">{name}</a></b> to text! {reason}',
                parse_mode="html",
            )
        else:
            await event.respond("This person can already speak freely!")
    elif mode == "unban":
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        unban = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, view_messages=True
        )
        if unban:
            await event.respond(f"Fine, they can join again.")
        else:
            await event.respond(
                "This person hasn't been banned... how am I meant to unban them?"
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
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        if event.chat.admin_rights.delete_messages:
            await reply_msg.delete()
    else:
        return await event.reply(
            "You have to reply to a message to delete it and ban the user."
        )
    await ban(event)


@Cbot(pattern="^/ban ?(.*)")
async def ban(event):
    if event.is_private:
        return
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
        await excecute_operation(event, user_id, user.first_name, mode, reason, 0)
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
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"ban|{user_id}|0"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/sban ?(.*)")
async def ban(event):
    if event.is_private:
        return
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
        await excecute_operation(event, user_id, user.first_name, mode, reason, 0)
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
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"sban|{user_id}|0"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@tbot.on(events.CallbackQuery(pattern=r"anonymous(\_(.*))"))
async def anon_admins(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    input = data.split("_", 1)[1]
    input = input.split("|", 3)
    mode = input[0]
    user_id = input[1]
    time = input[2]
    if not event.sender_id in ELITES:
        if not await cb_can_ban_users(event, event.sender_id):
            return
    first_name = (await tbot.get_entity(int(user_id))).first_name
    await event.delete()
    await excecute_operation(event, user_id, first_name, mode, "", time)


@Cbot(pattern="^/unban ?(.*)")
async def unban(event):
    if event.is_private:
        return
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
        await excecute_operation(event, user_id, user.first_name, mode, reason, 0)
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
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"unban|{user_id}|0"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/dmute ?(.*)")
async def dban(event):
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        if event.chat.admin_rights.delete_messages:
            await reply_msg.delete()
    else:
        return await event.reply(
            "You have to reply to a message to delete it and mute the user."
        )
    await mute(event)


@Cbot(pattern="^/mute ?(.*)")
async def mute(event):
    if event.is_private:
        return
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
        await excecute_operation(event, user_id, user.first_name, mode, reason, 0)
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
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"mute|{user_id}|0"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/smute ?(.*)")
async def ban(event):
    if event.is_private:
        return
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
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(event, user_id, user.first_name, mode, reason, 0)
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
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"smute|{user_id}|0"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/unmute ?(.*)")
async def unmute(event):
    if event.is_private:
        return
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
        await excecute_operation(event, user_id, user.first_name, mode, reason, 0)
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
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I unmute an admin? That sounds like a pretty dumb idea."
            )
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"unmute|{user_id}|0"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/dkick ?(.*)")
async def dban(event):
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        if event.chat.admin_rights.delete_messages:
            await reply_msg.delete()
    else:
        return await event.reply(
            "You have to reply to a message to delete it and kick the user."
        )
    await kick(event)


@Cbot(pattern="^/kick ?(.*)")
async def kick(event):
    if event.is_private:
        return
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
        await excecute_operation(event, user_id, user.first_name, mode, reason, 0)
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
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I kick an admin? That sounds like a pretty dumb idea."
            )
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"kick|{user_id}|0"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/skick ?(.*)")
async def ban(event):
    if event.is_private:
        return
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
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(event, user_id, user.first_name, mode, reason, 0)
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
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I kick an admin? That sounds like a pretty dumb idea."
            )
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"kick|{user_id}|0"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)


@Cbot(pattern="^/tban ?(.*)")
async def tban(event):
    if event.is_private:
        return
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
        if not reason:
            return
        if len(reason) == 1:
            return await event.reply("Lmao")
        tt = await extract_time(event, reason)
        user_id = user.id
        mode = "tban"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(event, user_id, user.first_name, mode, reason, int(tt))
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
            return
        if len(reason) == 1:
            return await event.reply("Lmao")
        tt = await extract_time(event, reason)
        user_id = user.id
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"tban|{user_id}|{tt}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)

@Cbot(pattern="^/tmute ?(.*)")
async def tban(event):
    if event.is_private:
        return
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
        if not reason:
            return
        if len(reason) == 1:
            return await event.reply("Lmao")
        tt = await extract_time(event, reason)
        user_id = user.id
        mode = "tmute"
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        await excecute_operation(event, user_id, user.first_name, mode, reason, int(tt))
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
            return
        if len(reason) == 1:
            return await event.reply("Lmao")
        tt = await extract_time(event, reason)
        user_id = user.id
        if await is_admin(event.chat_id, user_id):
            return await event.reply(
                "Why would I ban an admin? That sounds like a pretty dumb idea."
            )
        txt = (
            "It looks like you're anonymous. Tap this button to confirm your identity."
        )
        cb_data = f"tmute|{user_id}|{tt}"
        buttons = Button.inline(
            "Click to prove admin", data="anonymous_{}".format(cb_data)
        )
        await event.reply(txt, buttons=buttons)
