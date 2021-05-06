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
  await event.respond(nood)
  if args == 'text':
    await tbot.edit_permissions(event.chat_id, send_messages=False, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'sticker':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=False, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'preview':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=False, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'gif':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=False, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'game':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=False, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'inline':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=False, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'media':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=False, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'poll':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=False, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'invitelink':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=False)
