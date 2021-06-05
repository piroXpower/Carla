# soon
from Evelyn.events import Cbot
from Evelyn.modules.sql.locks_sql import get_chat_locks


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


async def delete_locked(event, locks=[]):
    if not event.chat.admin_rights.delete_messages:
        return
    if "sticker" in locks:
        if event.sticker:
            await event.delete()
    elif "gif" in locks:
        if event.gif:
            await event.delete()
    elif "phone" in locks:
        print("soon")
    elif "audio" in locks:
        if event.audio:
            await event.delete()
    elif "video" in locks:
        if event.video:
            await event.delete()
    elif "emoji" in locks:
        print("soon")
    if "inline" in locks:
        if event.via_bot_id:
            await event.delete()
    elif "emojigame" in locks:
        if event.media:
            if event.media.emoticon:
                if event.media.emoticon in ["🎰", "⚽", "🏀", "🎯", "🎲"]:
                    await event.delete()
