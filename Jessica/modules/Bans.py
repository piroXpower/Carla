import time

from telethon import Button

from Jessica import tbot
from Jessica.events import Cbot, Cinline

from . import (
    DEVS,
    can_ban_users,
    cb_can_ban_users,
    extract_time,
    g_time,
    get_user,
    is_admin,
)

db = {}


async def excecute_operation(
    event, user_id, name, mode, reason="", tt=0, reply_to=None, cb=False
):
    if reply_to == event.id:
        reply_to = event.reply_to_msg_id or event.id
    r = ""
    if reason:
        r = f"\nReason: <code>{reason}</code>"
    if name:
        name = ((name).replace("<", "&lt;")).replace(">", "&gt;")
    if event.chat.admin_rights:
        if not event.chat.admin_rights.ban_users:
            return await event.reply("I haven't got the rights to do this.")
    if user_id in DEVS and mode in ["ban", "tban", "mute", "tmute", "kick"]:
        return await event.reply("Sorry, I can't act against my devs!")
    if mode == "ban":
        await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, view_messages=False
        )
        if cb:
            await event.delete()
            reply_to = None
        await event.respond(
            f'Another one bites the dust...! Banned <a href="tg://user?id={user_id}">{name}</a></b>.{r}',
            parse_mode="html",
            reply_to=reply_to,
        )
    elif mode == "kick":
        await tbot.kick_participant(event.chat_id, int(user_id))
        if cb:
            await event.delete()
            reply_to = None
        await event.respond(
            f'I"ve kicked <a href="tg://user?id={user_id}">{name}</a></b>.{r}',
            parse_mode="html",
            reply_to=reply_to,
        )
    elif mode == "mute":
        await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, send_messages=False
        )
        if cb:
            await event.delete()
            reply_to = None
        await event.respond(
            f'Shhh... quiet now.\nMuted <a href="tg://user?id={user_id}">{name}</a>.{r}',
            parse_mode="html",
            reply_to=reply_to,
        )
    elif mode == "tban":
        if cb:
            await event.delete()
            reply_to = None
        await event.respond(
            f'Banned <a href="tg://user?id={user_id}">{name}</a> for {g_time(int(tt))}!',
            parse_mode="html",
            reply_to=reply_to,
        )
        await tbot.edit_permissions(
            event.chat_id,
            int(user_id),
            until_date=time.time() + int(tt),
            view_messages=False,
        )
    elif mode == "tmute":
        if cb:
            await event.delete()
            reply_to = None
        await event.respond(
            f'Muted <a href="tg://user?id={user_id}">{name}</a> for {g_time(int(tt))}!',
            parse_mode="html",
            reply_to=reply_to,
        )
        await tbot.edit_permissions(
            event.chat_id,
            int(user_id),
            until_date=time.time() + int(tt),
            send_messages=False,
        )
    elif mode == "unmute":
        if cb:
            await event.delete()
            reply_to = None
        unmute = await tbot.edit_permissions(
            event.chat_id, int(user_id), until_date=None, send_messages=True
        )
        if unmute:
            await event.respond(
                f'I shall allow <a href="tg://user?id={user_id}">{name}</a></b> to text! {r}',
                parse_mode="html",
                reply_to=reply_to,
            )
        else:
            await event.reply("This person can already speak freely!")
    elif mode == "unban":
        if cb:
            await event.delete()
            reply_to = None
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
    if not event.from_id:
        return await a_ban(event, "dban")
    if event.is_group:
        if not event.sender_id in DEVS:
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
    if await is_admin(event.chat_id, user.id):
        return await event.reply(
            "Why would I unmute an admin? That sounds like a pretty dumb idea."
        )
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "ban",
        reason,
        0,
        event.id,
    )


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
    if not event.from_id:
        return await a_ban(event, "ban")
    if event.is_group:
        if not event.sender_id in DEVS:
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
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "ban",
        reason,
        0,
        event.id,
    )


@Cbot(pattern="^/sban ?(.*)")
async def ban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await a_ban(event, "sban")
    if event.is_group:
        if not event.sender_id in DEVS:
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
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "sban",
        reason,
        0,
        event.id,
    )


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
    if not event.from_id:
        return await a_ban(event, "unban")
    if event.is_group:
        if not event.sender_id in DEVS:
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
            "Why would I unban an admin? That sounds like a pretty dumb idea."
        )
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "unban",
        reason,
        0,
        event.id,
    )


@Cbot(pattern="^/dmute ?(.*)")
async def dmute(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await a_ban(event, "dmute")
    if event.is_group:
        if not event.sender_id in DEVS:
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
    if await is_admin(event.chat_id, user.id):
        return await event.reply(
            "Why would I mute an admin? That sounds like a pretty dumb idea."
        )
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "mute",
        reason,
        0,
        event.id,
    )


@Cbot(pattern="^/mute ?(.*)")
async def mute(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await a_ban(event, "mute")
    if event.is_group:
        if not event.sender_id in DEVS:
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
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "mute",
        reason,
        0,
        event.id,
    )


@Cbot(pattern="^/smute ?(.*)")
async def smute(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await a_ban(event, "smute")
    if event.is_group:
        if not event.sender_id in DEVS:
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
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "smute",
        reason,
        0,
        event.id,
    )


@Cbot(pattern="^/unmute ?(.*)")
async def unmute(event):
    if (
        event.text.startswith(".unmuteall")
        or event.text.startswith("?unmuteall")
        or event.text.startswith("/unmuteall")
        or event.text.startswith("!unmuteall")
    ):
        return
    if not event.from_id:
        return await a_ban(event, "unmute")
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.is_group:
        if not event.sender_id in DEVS:
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
            "Why would I unmute an admin? That sounds like a pretty dumb idea."
        )
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "unmute",
        reason,
        0,
        event.id,
    )


@Cbot(pattern="^/dkick ?(.*)")
async def dban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await a_ban(event, "kick")
    if event.is_group:
        if not event.sender_id in DEVS:
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
    if await is_admin(event.chat_id, user.id):
        return await event.reply(
            "Why would I kick an admin? That sounds like a pretty dumb idea."
        )
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "kick",
        reason,
        0,
        event.id,
    )


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
    if not event.from_id:
        return await a_ban(event, "kick")
    if event.is_group:
        if not event.sender_id in DEVS:
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
            "Why would I kick an admin? That sounds like a pretty dumb idea."
        )
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "kick",
        reason,
        0,
        event.id,
    )


@Cbot(pattern="^/skick ?(.*)")
async def ban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await a_ban(event, "skick")
    if event.is_group:
        if not event.sender_id in DEVS:
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
    if await is_admin(event.chat_id, user_id):
        return await event.reply(
            "Why would I kick an admin? That sounds like a pretty dumb idea."
        )
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "skick",
        reason,
        0,
        event.id,
    )


@Cbot(pattern="^/tban ?(.*)")
async def tban(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await a_ban(event, "tban")
    if event.is_group:
        if not event.sender_id in DEVS:
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
        return await event.reply("You haven't specified a time to ban this user for!")
    if not reason[0].isdigit():
        return await event.reply(
            "failed to get specified time: {reason} is not a valid number"
        )
    if len(reason) == 1:
        return await event.reply(
            f"""failed to get specified time: '{reason}' does not follow the expected time patterns.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
        )
    ban_time = int(await extract_time(event, reason))
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "tban",
        reason,
        ban_time,
        event.id,
    )


@Cbot(pattern="^/tmute ?(.*)")
async def tmute(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await a_ban(event, "tmute")
    if event.is_group:
        if not event.sender_id in DEVS:
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
        return await event.reply("You haven't specified a time to ban this user for!")
    if not reason[0].isdigit():
        return await event.reply(
            "failed to get specified time: {reason} is not a valid number"
        )
    if len(reason) == 1:
        return await event.reply(
            f"""failed to get specified time: '{reason}' does not follow the expected time patterns.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
        )
    mute_time = await extract_time(event, reason)
    await excecute_operation(
        event,
        user.id,
        user.first_name,
        "tmute",
        reason,
        int(mute_time),
        event.id,
    )


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
    if event.from_id:
        if await is_admin(event.chat_id, event.sender_id):
            return await event.reply(
                "Ha, I'm not banning you, you're an admin! You're stuck with everyone here."
            )
    await event.reply("why making a scene just leave bitch!")


# -------Anonymous_Admins--------


async def a_ban(event, mode):
    user_id = None
    first_name = None
    e_t = None
    if event.reply_to:
        user = (await event.get_reply_message()).sender
        user_id = user.id
        first_name = user.first_name
    elif event.pattern_match.group(1):
        u_obj = event.text.split(None, 2)[1]
        try:
            user = await tbot.get_entity(u_obj)
            user_id = user.id
            first_name = user.first_name
        except:
            pass
    try:
        if event.reply_to:
            e_t = event.text.split(None, 1)[1]
        elif user_id:
            e_t = event.text.split(None, 2)[2]
    except IndexError:
        e_t = None
    db[event.id] = [e_t, user_id, first_name]
    cb_data = str(event.id) + "|" + str(mode)
    a_buttons = Button.inline("Click to prove admin", data="banon_{}".format(cb_data))
    await event.reply(
        "It looks like you're anonymous. Tap this button to confirm your identity.",
        buttons=a_buttons,
    )


@Cinline(pattern=r"banon(\_(.*))")
async def rules_anon(e):
    if not await cb_can_ban_users(e, e.sender_id):
        return
    d_ata = ((e.pattern_match.group(1)).decode()).split("_", 1)[1]
    da_ta = d_ata.split("|", 1)
    event_id = int(da_ta[0])
    mode = da_ta[1]
    try:
        cb_data = db[event_id]
    except KeyError:
        return await e.edit("This requests has been expired.")
    user_id = cb_data[1]
    fname = cb_data[2]
    reason = cb_data[0]
    mute_time = 0
    if not reason:
        reason = ""
    if not user_id:
        return await e.edit(
            "I don't know who you're talking about, you're going to need to specify a user...!"
        )
    if await is_admin(e.chat_id, user_id):
        return await e.edit(
            "Why would I {} an admin? That sounds like a pretty dumb idea.".format(mode)
        )
    if mode in ["tban", "tmute"]:
        if not reason:
            return await e.edit(
                "You haven't specified a time to ban/mute this user for!"
            )
        if not reason[0].isdigit():
            return await e.edit(
                "failed to get specified time: {reason} is not a valid number"
            )
        if len(reason) == 1:
            return await e.edit(
                f"""failed to get specified time: '{reason}' does not follow the expected time patterns.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
            )
        mute_time = await extract_time(e, reason)
    await excecute_operation(
        e,
        user_id,
        fname,
        mode,
        reason,
        mute_time,
        None,
        True,
    )
