# soon
from Evelyn.events import Cbot
from Evelyn.modules.sql.locks_sql import get_chat_locks


@Cbot(pattern="^/locktypes")
async def lt(event):
    text = """
The available locktypes are:
- all
- audio
- bot
- button
- command
- contact
- document
- emojigame
- forward
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
- voice
"""
    await event.reply(text)


ok_locks = """
These are the current lock settings:
- all = {}
- album =false
- audio = {}
- bot = {}
- button = {}
- command = {}
- contact = {}
- document = {}
- email = false
- emojigame = {}
- forward = {}
- game = false
- gif = {}
- inline = {}
- invitelink = {}
- location = {}
- phone = {}
- photo = {}
- poll = false
- sticker = {}
- text =false
- url = {}
- video = {}
- videonote = false
- voice = false
"""


@Cbot(pattern="^/locks")
async def locks(event):
    c = get_chat_locks(event.chat_id)
    final_y = ok_locks.format(
        c.all,
        c.audio,
        c.bot,
        c.button,
        c.command,
        c.contact,
        c.document,
        c.emojigame,
        c.forward,
        c.gif,
        c.inline,
        c.invitelink,
        c.location,
        c.phone,
        c.photo,
        c.sticker,
        c.url,
        c.video,
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
