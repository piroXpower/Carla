from Carla import tbot
from telethon import Button, events
from . import is_admin

ltext = """
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

@Cbot(pattern="^/locktypes ?(.*)")
async def _(event):
 if event.is_private:
   await event.respond(ltext)
 if event.is_group:
   if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("You need to be an admin to do this.")
   await event.reply(ltext)
