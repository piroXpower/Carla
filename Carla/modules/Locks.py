from Carla import tbot
from telethon import Button, events
from . import is_admin, can_change_info

supported = ["all", "media", "game", "gif", "inline", "invitelink", "poll", "preview", "sticker", "text"]

ltext = """
The available locktypes are:
- all
- game
- gif
- inline
- invitelink
- media
- poll
- preview
- sticker
- text
"""

lockie = """
These are the current lock settings:
- all = {}
- text = {}
- media = {}
- poll = {}
- gif = {}
- sticker = {}
- game = {}
- preview = {}
- invitelink = {}
- inline = {}
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
 if event.text.startswith("!locktypes") or event.text.startswith("/locktypes") or event.text.startswith("?locktypes") or event.text.startswith("!locks") or event.text.startswith("?locks") or event.text.startswith("/locks"):
   return
 if event.is_private:
   return #connect
 if not await can_change_info(event, event.sender_id):
   return
 args = event.pattern_match.group(1)
 if not args:
       return await event.reply("You haven't specified a type to lock.")
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
  elif args == 'all':
    await tbot.edit_permissions(event.chat_id, send_messages=False, send_gifs=False, send_games=False, send_stickers=False, send_inline=False, embed_link_previews=False, send_polls=False, invite_users=False, send_media=False)

@Cbot(pattern="^/unlock ?(.*)")
async def _(event):
 if event.text.startswith("!locktypes") or event.text.startswith("/locktypes") or event.text.startswith("?locktypes") or event.text.startswith("!locks") or event.text.startswith("?locks") or event.text.startswith("/locks"):
   return
 if event.is_private:
   return #connect
 if not await can_change_info(event, event.sender_id):
   return
 args = event.pattern_match.group(1)
 if not args:
       return await event.reply("You haven't specified a type to unlock.")
 if not args in supported:
      return await event.reply(f"Unknown lock types:\n- {args}\nCheck /locktypes!")
 await chat_ul(event, args)

async def chat_ul(event, args):
  nood = "Unlocked `{}`.".format(args)
  await event.respond(nood)
  if args == 'text':
    await tbot.edit_permissions(event.chat_id, send_messages=True, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'sticker':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=True, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'preview':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=True, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'gif':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=True, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'game':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=True, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'inline':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=True, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'media':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=True, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'poll':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=True, invite_users=not event.chat.default_banned_rights.invite_users)
  elif args == 'invitelink':
    await tbot.edit_permissions(event.chat_id, send_messages=not event.chat.default_banned_rights.send_messages, send_gifs=not event.chat.default_banned_rights.send_gifs, send_stickers=not event.chat.default_banned_rights.send_stickers, send_games=not event.chat.default_banned_rights.send_games, embed_link_previews=not event.chat.default_banned_rights.embed_links, send_inline=not event.chat.default_banned_rights.send_inline, send_media=not event.chat.default_banned_rights.send_media, send_polls=not event.chat.default_banned_rights.send_polls, invite_users=True)
  elif args == 'all':
    await tbot.edit_permissions(event.chat_id, send_messages=True, send_gifs=True, send_games=True, send_stickers=True, send_inline=True, embed_link_previews=True, send_polls=True, invite_users=True, send_media=True)


@Cbot(pattern="^/locks")
async def _(event):
 if event.is_private:
   return #connect
 if event.is_group:
   if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("You need to be an admin to do this.")
 cl = event.chat.default_banned_rights
 gey = False
 if cl.send_messages==cl.send_media==cl.send_polls==cl.send_gifs==cl.send_stickers==cl.send_games==cl.embed_links==cl.invite_users==cl.send_inline==True:
    gey = True
 satta = lockie.format(gey, cl.send_messages, cl.send_media, cl.send_polls, cl.send_gifs, cl.send_stickers, cl.send_games, cl.embed_links, cl.invite_users, cl.send_inline)
 await event.respond(satta)
