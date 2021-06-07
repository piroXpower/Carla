# soon
from telethon import events

from Evelyn import tbot
from Evelyn.events import Cbot
from Evelyn.modules.sql.locks_sql import add_lock, get_chat_locks, remove_lock

from . import can_change_info, is_admin


@Cbot(pattern="^/locktypes")
async def lt(event):
    text = """
The available locktypes are:
- all
- audio
- album
- bot
- button
- command
- contact
- document
- email
- emojigame
- forward
- game
- gif
- inline
- invitelink
- location
- phone
- photo
- poll
- sticker
- text
- url
- video
- videonote
- voice
"""
    await event.reply(text)


ok_locks = """
These are the current lock settings:
- all = {}
- album = false
- audio = {}
- bot = {}
- button = {}
- command = {}
- contact = {}
- document = {}
- email = {}
- emojigame = {}
- forward = {}
- game = {}
- gif = {}
- inline = {}
- invitelink = {}
- location = {}
- phone = {}
- photo = {}
- poll = {}
- sticker = {}
- text = {}
- url = {}
- video = {}
- videonote = {}
- voice = {}
"""


@Cbot(pattern="^/locks")
async def locks(event):
    c = get_chat_locks(event.chat_id)
    final_y = ok_locks.format(
        str(c.all).lower(),
        str(c.audio).lower(),
        str(c.bot).lower(),
        str(c.button).lower(),
        str(c.command).lower(),
        str(c.contact).lower(),
        str(c.document).lower(),
        str(c.email).lower(),
        str(c.emojigame).lower(),
        str(c.forward).lower(),
        str(c.game).lower(),
        str(c.gif).lower(),
        str(c.inline).lower(),
        str(c.invitelink).lower(),
        str(c.location).lower(),
        str(c.phone).lower(),
        str(c.photo).lower(),
        str(c.poll).lower(),
        str(c.sticker).lower(),
        str(c.text).lower(),
        str(c.url).lower(),
        str(c.video).lower(),
        str(c.videonote).lower(),
        str(c.voice).lower(),
    )
    await event.reply(final_y)


lock_types = [
    "all",
    "audio",
    "media",
    "bot",
    "button",
    "command",
    "contact",
    "document",
    "email",
    "emojigame",
    "forward",
    "game",
    "gif",
    "inline",
    "invitelink",
    "location",
    "phone",
    "photo",
    "poll",
    "sticker",
    "text",
    "url",
    "video",
    "videonote",
    "voice",
]


@Cbot(pattern="^/lock ?(.*)")
async def lock(event):
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
        return
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    lock = event.pattern_match.group(1)
    if not lock in lock_types:
        return await event.reply(
            f"""Unknown lock types:
- {lock}
Check /locktypes!"""
        )
    await event.reply(f"Locked `{lock}`.")
    if lock == "all":
        add_lock(event.chat_id, all=True)
    elif lock == "audio":
        add_lock(event.chat_id, audio=True)
    elif lock == "media":
        add_lock(event.chat_id, media=True)
    elif lock == "bot":
        add_lock(event.chat_id, bot=True)
    elif lock == "button":
        add_lock(event.chat_id, button=True)
    elif lock == "command":
        add_lock(event.chat_id, command=True)
    elif lock == "contact":
        add_lock(event.chat_id, contact=True)
    elif lock == "document":
        add_lock(event.chat_id, document=True)
    elif lock == "email":
        add_lock(event.chat_id, email=True)
    elif lock == "emojigame":
        add_lock(event.chat_id, emojigame=True)
    elif lock == "forward":
        add_lock(event.chat_id, forward=True)
    elif lock == "game":
        add_lock(event.chat_id, game=True)
    elif lock == "gif":
        add_lock(event.chat_id, gif=True)
    elif lock == "inline":
        add_lock(event.chat_id, inline=True)
    elif lock == "invitelink":
        add_lock(event.chat_id, invitelink=True)
    elif lock == "location":
        add_lock(event.chat_id, location=True)
    elif lock == "phone":
        add_lock(event.chat_id, phone=True)
    elif lock == "photo":
        add_lock(event.chat_id, photo=True)
    elif lock == "poll":
        add_lock(event.chat_id, poll=True)
    elif lock == "sticker":
        add_lock(event.chat_id, sticker=True)
    elif lock == "text":
        add_lock(event.chat_id, text=True)
    elif lock == "url":
        add_lock(event.chat_id, url=True)
    elif lock == "video":
        add_lock(event.chat_id, video=True)
    elif lock == "videonote":
        add_lock(event.chat_id, videonote=True)
    elif lock == "voice":
        add_lock(event.chat_id, voice=True)


@Cbot(pattern="^/unlock ?(.*)")
async def lock(event):
    if event.is_private:
        return
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    lock = event.pattern_match.group(1)
    if not lock in lock_types:
        return await event.reply(
            f"""Unknown lock types:
- {lock}
Check /locktypes!"""
        )
    await event.reply(f"Unlocked `{lock}`.")
    if lock == "all":
        remove_lock(
            event.chat_id,
            all=False,
            audio=False,
            media=False,
            bot=False,
            button=False,
            command=False,
            contact=False,
            document=False,
            email=False,
            emojigame=False,
            forward=False,
            game=False,
            gif=False,
            inline=False,
            invitelink=False,
            location=False,
            phone=False,
            photo=False,
            poll=False,
            sticker=False,
            text=False,
            url=False,
            video=False,
            videonote=False,
            voice=False,
        )
    elif lock == "audio":
        remove_lock(event.chat_id, audio=False)
    elif lock == "media":
        remove_lock(event.chat_id, media=False)
    elif lock == "bot":
        remove_lock(event.chat_id, bot=False)
    elif lock == "button":
        remove_lock(event.chat_id, button=False)
    elif lock == "command":
        remove_lock(event.chat_id, command=False)
    elif lock == "contact":
        remove_lock(event.chat_id, contact=False)
    elif lock == "document":
        remove_lock(event.chat_id, document=False)
    elif lock == "email":
        remove_lock(event.chat_id, email=False)
    elif lock == "emojigame":
        remove_lock(event.chat_id, emojigame=False)
    elif lock == "forward":
        remove_lock(event.chat_id, forward=False)
    elif lock == "game":
        remove_lock(event.chat_id, game=False)
    elif lock == "gif":
        remove_lock(event.chat_id, gif=False)
    elif lock == "inline":
        remove_lock(event.chat_id, inline=False)
    elif lock == "invitelink":
        remove_lock(event.chat_id, invitelink=False)
    elif lock == "location":
        remove_lock(event.chat_id, location=False)
    elif lock == "phone":
        remove_lock(event.chat_id, phone=False)
    elif lock == "photo":
        remove_lock(event.chat_id, photo=False)
    elif lock == "poll":
        remove_lock(event.chat_id, poll=False)
    elif lock == "sticker":
        remove_lock(event.chat_id, sticker=False)
    elif lock == "text":
        remove_lock(event.chat_id, text=False)
    elif lock == "url":
        remove_lock(event.chat_id, url=False)
    elif lock == "video":
        remove_lock(event.chat_id, video=False)
    elif lock == "videonote":
        remove_lock(event.chat_id, videonote=False)
    elif lock == "voice":
        remove_lock(event.chat_id, voice=False)


@tbot.on(events.NewMessage(pattern="plock"))
async def msg(event):
    if not event.is_group:
        return
    if not await is_admin(event.chat_id, event.sender_id):
        return
    locked = []
    lock = get_chat_locks(event.chat_id)
    if lock.all:
        locked = lock_types
    else:
        if lock.audio:
            locked.append("audio")
        if lock.media:
            locked.append("media")
        if lock.bot:
            locked.append("bot")
        if lock.button:
            locked.append("button")
        if lock.command:
            locked.append("command")
        if lock.contact:
            locked.append("contact")
        if lock.document:
            locked.append("document")
        if lock.email:
            locked.append("email")
        if lock.emojigame:
            locked.append("emojigame")
        if lock.forward:
            locked.append("forward")
        if lock.game:
            locked.append("game")
        if lock.gif:
            locked.append("gif")
        if lock.inline:
            locked.append("inline")
        if lock.invitelink:
            locked.append("invitelink")
        if lock.location:
            locked.append("location")
        if lock.phone:
            locked.append("phone")
        if lock.photo:
            locked.append("photo")
        if lock.poll:
            locked.append("poll")
        if lock.sticker:
            locked.append("sticker")
        if lock.text:
            locked.append("text")
        if lock.url:
            locked.append("url")
        if lock.video:
            locked.append("video")
        if lock.videonote:
            locked.append("videonote")
        if lock.voice:
            locked.append("voice")
    if not event.chat.admin_rights.ban_users:
        return
    if "sticker" in locked:
        if event.sticker:
            await event.delete()
    if "gif" in locked:
        if event.gif:
            await event.delete()
    if "document" in locked:
        if event.document:
            await event.delete()
