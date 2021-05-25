from Evelyn import tbot

from . import g_time


async def excecute_operation(
    event, user_id, name, mode, reason="", tt=0, attributes=""
):
    if mode == "ban":
        if attributes == "d":
            await event.delete()
        await tbot.edit_permissions(
            event.chat_id, user_id, until_date=None, view_messages=False
        )
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        if not attributes == "s":
            await event.respond(
                f'Another one bites the dust...! Banned <a href="tg://user?id={user_id}">{name}</a></b>.{reason}',
                parse_mode="html",
            )
    elif mode == "kick":
        await tbot.kick_participant(event.chat_id, event.sender_id)
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        await event.respond(
            f'I"ve kicked <a href="tg://user?id={user_id}">{name}</a></b>.{reason}',
            parse_mode="html",
        )
    elif mode == "mute":
        await tbot.edit_permissions(
            event.chat_id, event.sender_id, until_date=None, send_messages=False
        )
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        await event.respond(
            f'<b>Muted <a href="tg://user?id={user_id}">{name}</a></b>!{reason}',
            parse_mode="html",
        )
    elif mode == "tban":
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        time = g_time(tt)
        await event.respond(
            f'<b>Banned <a href="tg://user?id={user_id}">{name}</a></b> for {time}!{reason}',
            parse_mode="html",
        )
        await tbot.edit_permissions(
            event.chat_id,
            event.sender_id,
            until_date=time.time() + int(tt),
            view_messages=False,
        )
    elif mode == "tmute":
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        time = g_time(tt)
        await event.respond(
            f'<b>Muted <a href="tg://user?id={user_id}">{name}</a></b> for {time}!{reason}',
            parse_mode="html",
        )
        await tbot.edit_permissions(
            event.chat_id,
            event.sender_id,
            until_date=time.time() + int(tt),
            send_messages=False,
        )
    elif mode == "unmute":
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        unmute = await tbot.edit_permissions(
            event.chat_id, event.sender_id, until_date=None, send_messages=True
        )
        if unmute:
            await event.respond(
                f'I shall allow <a href="tg://user?id={user_id}">{name}</a></b> to text! {reason}',
                parse_mode="html",
            )
        else:
            await event.reply("This person can already speak freely!")
    elif mode == "unban":
        if reason:
            reason = f"\nReason: <code>{reason}</code>"
        unban = await tbot.edit_permissions(
            event.chat_id, event.sender_id, until_date=None, view_messages=True
        )
        if unban:
            await event.respond(f"Fine, they can join again.")
        else:
            await event.reply(
                "This person hasn't been banned... how am I meant to unban them?"
            )
