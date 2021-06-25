from telethon import events

import Jessica.modules.mongodb.locks_db as db
from Jessica import tbot
from Jessica.events import Cbot

from . import can_change_info


@Cbot(pattern="^/lock ?(.*)")
async def lock_item(event):
    if (
        event.text.startswith(".locks")
        or event.text.startswith("/locks")
        or event.text.startswith("!locks")
        or event.text.startswith("?locks")
        or event.text.startswith(".locktypes")
        or event.text.startswith("/locktypes")
        or event.text.startswith("?locktypes")
        or event.text.startswith("!locktypes")
    ):
        return
    if event.is_private:
        return await event.reply("This command is made to be used in group chats.")
    if event.is_group and event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    if not event.pattern_match.group(1):
        return await event.reply("You haven't specified a type to lock.")
    try:
        lock_items = event.text.split(None, 1)[1]
    except IndexError:
        return await event.reply("You haven't specified a type to lock.")
    locks = lock_items.split(None)
    lock_s = []
    av_locks = db.all_locks
    for lock in locks:
        if lock in av_locks:
            lock_s.append(lock)
    if "all" in lock_s:
        db.lock_all(event.chat_id)
        await event.reply("Locked `all`")
        try:
            await tbot.edit_permissions(event.chat_id, send_messages=False)
        except Exception as e:
            print(e)
        return
    if len(lock_s) == 0:
        await event.reply(f"Unknown lock types:- {lock_items}\nCheck /locktypes!")
    else:
        text = "Locked"
        for i in lock_s:
            text = text + f" `{i}`"
        await event.reply(text)
    for lock in lock_s:
        db.add_lock(event.chat_id, lock)
    if "text" in lock_s:
        try:
            await tbot.edit_permissions(event.chat_id, send_messages=False)
        except:
            pass
    if "media" in lock_s:
        try:
            await tbot.edit_permissions(event.chat_id, send_media=False)
        except:
            pass
    if "inline" in lock_s:
        try:
            await tbot.edit_permissions(event.chat_id, send_inline=False)
        except:
            pass


@Cbot(pattern="^/locktypes")
async def lock_types(event):
    main_txt = "The avaliable lock types are:"
    av_locks = db.all_locks
    for x in av_locks:
        main_txt = main_txt + "\n- " + x
    await event.reply(main_txt)


@Cbot(pattern="^/locks")
async def locks(event):
    if not await can_change_info(event, event.sender_id):
        return
    av_locks = db.all_locks
    _final = "These are the current lock settings:"
    locked = db.get_locks(event.chat_id)
    for x in av_locks:
        _mode = "false"
        if x in locked:
            _mode = "true"
        _final = _final + "\n- " + x + " = " + _mode
    await event.reply(_final)


@Cbot(pattern="^/unlock ?(.*)")
async def unlock_item(event):
    if event.is_private:
        return await event.reply("This command is made to be used in group chats.")
    if event.is_group and event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    if not event.from_id:
        return await a_locks(event, "unlock")
    if not event.pattern_match.group(1):
        return await event.reply("You haven't specified a type to unlock.")
    try:
        unlock_items = event.text.split(None, 1)[1]
    except IndexError:
        return await event.reply("You haven't specified a type to unlock.")
    unlocks = unlock_items.split(None)
    unlock_s = []
    av_locks = db.all_locks
    for unlock in unlocks:
        if unlock in av_locks:
            unlock_s.append(unlock)
    if "all" in unlock_s:
        db.unlock_all(event.chat_id)
        await event.reply("Unlocked `all`")
        try:
            await tbot.edit_permissions(event.chat_id, send_messages=True)
        except:
            pass
        return
    if len(unlock_s) == 0:
        await event.reply(f"Unknown lock types:- {lock_items}\nCheck /locktypes!")
    else:
        text = "Unlocked"
        for i in unlock_s:
            text = text + f" `{i}`"
        await event.reply(text)
    for lock in unlock_s:
        db.remove_lock(event.chat_id, lock)
    if "text" in unlock_s:
        try:
            await tbot.edit_permissions(event.chat_id, send_messages=True)
        except:
            pass
    if "media" in unlock_s:
        try:
            await tbot.edit_permissions(event.chat_id, send_media=True)
        except:
            pass
    if "inline" in unlock_s:
        try:
            await tbot.edit_permissions(event.chat_id, send_inline=True)
        except:
            pass


@tbot.on(events.NewMessage())
async def locks(event):
    if not event.chat.admin_rights.delete_messages:
        return
    locked = db.get_locks
    if len(locked) == 0:
        return
    trigg = await lock_check(event, locked)
    print(trigg)


async def lock_check(event, locked):
    trigg = False
    if "sticker" in locked:
        if event.sticker:
            trigg = True
    if "gif" in locked:
        if event.gif:
            trigg = True
    if "document" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaDocument):
                if not event.media.document.mime_type in [
                    "image/webp",
                    "application/x-tgsticker",
                    "image/jpeg",
                    "audio/ogg",
                    "audio/m4a",
                    "audio/mp3",
                    "video/mp4",
                ]:
                    trigg = True
    if "location" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaGeo):
                trigg = True
    if "phone" in locked:
        if event.message.entities:
            if isinstance(event.message.entities[0], MessageEntityPhone):
                trigg = True
    if "email" in locked:
        if event.message.entities:
            if isinstance(event.message.entities[0], MessageEntityEmail):
                trigg = True
    if "command" in locked:
        if event.message.entities:
            if isinstance(event.message.entities[0], MessageEntityBotCommand):
                trigg = True
    if "url" in locked:
        if event.message.entities:
            if isinstance(event.message.entities[0], MessageEntityUrl):
                trigg = True
    if "invitelink" in locked:
        if event.text:
            if "t.me/" in event.text:
                trigg = True
    if "poll" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaPoll):
                trigg = True
    if "photo" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaPhoto):
                trigg = True
    if "videonote" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaDocument):
                if event.media.document.mime_type == "video/mp4":
                    trigg = True
    if "video" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaDocument):
                if isinstance(
                    event.media.document.attributes[0], DocumentAttributeVideo
                ):
                    trigg = True
    if "voice" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaDocument):
                if isinstance(
                    event.media.document.attributes[0], DocumentAttributeAudio
                ):
                    if event.media.document.attributes[0].voice:
                        trigg = True
    if "audio" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaDocument):
                if isinstance(
                    event.media.document.attributes[0], DocumentAttributeAudio
                ):
                    trigg = True
    if "bot" in locked:
        if event.sender.bot:
            trigg = True
    if "button" in locked:
        if event.reply_markup:
            trigg = True
    if "game" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaGame):
                trigg = True
    if "contact" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaContact):
                trigg = True
    if "forward" in locked:
        if event.fwd_from:
            trigg = True
    if "emojigame" in locked:
        if event.media:
            if isinstance(event.media, MessageMediaDice):
                trigg = True
    if "forwardchannel" in locked:
        if event.fwd_from:
            if event.fwd_from.from_id:
                if isinstance(event.fwd_from.from_id, PeerChannel):
                    trigg = True
    return trigg
