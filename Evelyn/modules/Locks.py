# soon
from Evelyn.events import Cbot


@Cbot(pattern="^/locktypes")
async def lt(event):
    text = """
The available locktypes are:
- all
- album
- audio
- bot
- button
- command
- comment
- contact
- document
- email
- emojigame
- forward
- forwardbot
- forwardchannel
- forwarduser
- game
- gif
- inline
- invitelink
- location
- phone
- photo
- poll
- rtl
- sticker
- text
- url
- video
- videonote
- voice
"""
    await event.reply(text)


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
