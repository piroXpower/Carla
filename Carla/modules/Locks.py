from Carla import tbot
from telethon import Button, events
from . import is_admin, can_change_info

supported = ["all", "album", "media", "audio", "bot", "button", "command", "contact", "document", "email", "emojigame", "forward", "forwardbot", "forwardchannel", "game", "gif", "inline", "invitelink", "location", "phone", "photo", "poll", "rtl", "sticker", "text", "url", "video", "voicenote", "voice"]

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
- media
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

@Cbot(pattern="^/lock ?(.*)")
async def _(event):
 if event.text.startswith("!locktypes") or event.text.startswith("/locktypes") or event.text.startswith("?locktypes"):
   return
 if event.is_private:
   return #connect
 if not await can_change_info(event, event.sender_id):
   return
 args = event.pattern_match.group(1)
 if not args in supported:
      return await event.reply(f"Unknown lock types:\n- {args}\nCheck /locktypes!")
 chat_rights = ["text", "gif", "sticker", "game", "inline", "media", "rtl", "poll", "invitelink"]
 if args in chat_rights:
   await chat_event(event, args)
 else:
   await db_lock(event, args)

async def chat_event(event, args):
 text = "Locked `{}`.".format(args)
 if args == 'text':
   await tbot.edit_permissions(event.chat_id, send_messages=False)
 elif args == 'gif':
   await tbot.edit_permissions(event.chat_id, send_gifs=False)
 elif args == 'sticker':
   await tbot.edit_permissions(event.chat_id, send_stickers=False)
 elif args == 'rtl':
   await tbot.edit_permissions(event.chat_id, embed_link_previews=False)
 elif args == 'game':
   await tbot.edit_permissions(event.chat_id, send_games=False)
 elif args == 'inline':
   await tbot.edit_permissions(event.chat_id, send_inline=False)
 elif args == 'media':
   await tbot.edit_permissions(event.chat_id, send_media=False)
 elif args == 'poll':
   await tbot.edit_permissions(event.chat_id, send_polls=False)
 elif args == 'invitelink':
   await tbot.edit_permissions(event.chat_id, invite_users=False)
 await event.respond(text)

async def db_lock(event, args):
 print(7)
