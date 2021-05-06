from Carla import tbot
from telethon import Button, events
from . import is_admin, can_change_info

supported = ["all", "media", "game", "gif", "inline", "invitelink", "poll", "rtl", "sticker", "text"]

ltext = """
The available locktypes are:
- all
- game
- gif
- inline
- invitelink
- media
- poll
- rtl
- sticker
- text
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
 await chat_event(event, args)

async def chat_event(event, args):
 nood = "Locked `{}`.".format(args)
 if args == 'text':
   await tbot.edit_permissions(event.chat_id, send_messages=False, send_gifs=None, send_stickers=None, send_games=None, embed_link_previews=None, send_inline=None, send_media=None, send_polls=None, invite_users=None)
 elif args == 'gif':
   await tbot.edit_permissions(event.chat_id, send_messages=None, send_gifs=False, send_stickers=None, send_games=None, embed_link_previews=None, send_inline=None, send_media=None, send_polls=None, invite_users=None)
 elif args == 'sticker':
   await tbot.edit_permissions(event.chat_id, send_messages=None, send_gifs=None, send_stickers=False, send_games=None, embed_link_previews=None, send_inline=None, send_media=None, send_polls=None, invite_users=None)
 elif args == 'rtl':
   await tbot.edit_permissions(event.chat_id, send_messages=None, send_gifs=None, send_stickers=None, send_games=None, embed_link_previews=False, send_inline=None, send_media=None, send_polls=None, invite_users=None)
 elif args == 'game':
   await tbot.edit_permissions(event.chat_id, send_messages=None, send_gifs=None, send_stickers=None, send_games=False, embed_link_previews=None, send_inline=None, send_media=None, send_polls=None, invite_users=None)
 elif args == 'inline':
   await tbot.edit_permissions(event.chat_id, send_messages=None, send_gifs=None, send_stickers=None, send_games=None, embed_link_previews=None, send_inline=False, send_media=None, send_polls=None, invite_users=None)
 elif args == 'media':
   await tbot.edit_permissions(event.chat_id, send_messages=None, send_gifs=None, send_stickers=None, send_games=None, embed_link_previews=None, send_inline=None, send_media=False, send_polls=None, invite_users=None)
 elif args == 'poll':
   await tbot.edit_permissions(event.chat_id, send_messages=None, send_gifs=None, send_stickers=None, send_games=None, embed_link_previews=None, send_inline=None, send_media=None, send_polls=False, invite_users=None)
 elif args == 'invitelink':
   await tbot.edit_permissions(event.chat_id, send_messages=None, send_gifs=None, send_stickers=None, send_games=None, embed_link_previews=None, send_inline=None, send_media=None, send_polls=None, invite_users=False)
 await event.respond(nood)
