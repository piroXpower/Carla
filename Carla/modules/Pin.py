from telethon import Button, events, types
from Carla import tbot, BOT_ID, OWNER_ID
from . import is_admin, can_pin_messages, ELITES
from Carla.events import Cbot

@Cbot(pattern="^/pinned")
async def _(event):
 if event.is_private:
  return #connect
 x = await event.reply("`Getting the pinned message..`")
 try:
     message = await tbot.get_messages(event.chat_id, ids=types.InputMessagePinned())
     id = message.id
 except AttributeError:
     return await x.edit("There are no pinned messages in this chat.")
 if event.chat.username:
     await x.edit(f"The pinned message in **{event.chat.title}** is **[Here]**(http://t.me/{event.chat.username}/{id}).", link_preview=False)
 else:
     chat_id = str(event.chat_id)
     chat_id = chat_id.replace('-100', '')
     await x.edit(f"The pinned message in **{event.chat.title}** is [here](http://t.me/c/{chat_id}/{id}).", link_preview=False)

@Cbot(pattern="^/pin ?(.*)")
async def _(event):
 virulent = ["silent", "violent", "notify", "loud", "quiet"]
 if event.text.startswith("?pinned") or event.text.startswith("!pinned") or event.text.startswith("/pinned"):
  return
 if event.is_private:
  return #connect
 if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
    await can_pin_messages(event, event.sender_id)
 if not event.reply_to_msg_id:
   return await event.reply("You need to reply to a message to pin it!")
 reply_msg = await event.get_reply_message()
 options = event.pattern_match.group(1)
 if options and options not in virulent:
        return await event.reply(f"'{options}' was not recognised as a valid pin option. Please use one of: loud/violent/notify/silent/quiet")
 is_silent = True
 if options == 'silent' or options == 'quiet':
   is_silent = False
 chat = (str(event.chat_id)).replace('-100', '')
 text = f"I have pinned [this message](t.me/c/{chat}/{reply_msg.id})."
 if options == 'notify':
  text = f"I have pinned [this message](t.me/c/{chat}/{reply_msg.id}). and notified all members."
 try:
      await tbot.pin_message(event.chat_id, reply_msg.id, notify=is_silent)
      if is_silent:
       await event.respond(text)
 except:
      await event.reply(f"Looks like I dont have permission to pin messages. Could you please promote me?")

@Cbot(pattern="^/unpin ?(.*)")
async def _(event):
 if event.text.startswith("?unpinall") or event.text.startswith("!unpinall") or event.text.startswith("/unpinall"):
  return
 if event.is_private:
  return #connect
 if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
    await can_pin_messages(event, event.sender_id)
 if not event.reply_to_msg_id:
  msg = await tbot.get_messages(event.chat_id, ids=types.InputMessagePinned())
  id = msg.id
  text = f"I have unpinned the last pinned message."
 else:
  reply = await event.get_reply_message()
  id = reply.id
  chat = (str(event.chat_id)).replace('-100', '')
  text = f"I have unpinned [this message](t.me/c/{chat}/{reply.id})."
 try:
  await tbot.unpin_message(event.chat_id, id)
  await event.respond(text)
 except:
  await event.reply(f"Looks like I dont have permission to pin messages. Could you please promote me?")
  
@Cbot(pattern="^/permapin ?(.*)")
async def _(event):
 args = event.pattern_match.group(1)
 if event.text.startswith("?unpinall") or event.text.startswith("!unpinall") or event.text.startswith("/unpinall"):
  return
 if event.is_private:
  return #connect
 if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
    await can_pin_messages(event, event.sender_id)
 if not args and not event.reply_to_msg_id:
  return await event.reply("You need to give some message content to pin!")
 is_silent = True
 if event.reply_to_msg_id:
    reply_msg = await event.get_reply_message()
    lolz = await event.respond(reply_msg)
    msg_id = lolz.id
    if args == 'silent' or args == 'quiet':
       is_silent = False
 elif not event.reply_to_msg_id and args:
    reply_msg = await event.respond(args)
    msg_id = reply_msg.id
 try:
    await tbot.pin_message(event.chat_id, msg_id, notify=is_silent)
 except:
    await event.reply("Looks like I dont have permission to pin messages. Could you please promote me?")
 
@Cbot(pattern="^/unpinall")
async def upinall(event):
  if event.is_private:
      return #connect
  if not await is_admin(event.chat_id, event.sender_id):
      return await event.reply("You need to be an admin to do this.")
  perm = await tbot.get_permissions(event.chat_id, event.sender_id)
  if not perm.is_creator:
    return await event.reply(f"You need to be the Creator of {event.chat.title} to do this.")
  text = "Are you sure you want to unpin all messages?"
  buttons = [Button.inline('Yes', data='upin'),Button.inline('No', data='cpin')]
  await event.respond(text, buttons=buttons)

@tbot.on(events.CallbackQuery(pattern=r"cpin"))
async def start_again(event):
        if not await is_admin(event.chat_id, event.sender_id):
          return await event.answer("You need to be an admin to do this!")
        permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not permissions.is_creator:
          return await event.answer("Only for chat creator")
        await event.edit("Unpin of all pinned messages has been cancelled.", buttons=None)

@tbot.on(events.CallbackQuery(pattern=r"upin"))
async def start_again(event):
        if not await is_admin(event.chat_id, event.sender_id):
          return await event.answer("You need to be an admin to do this!")
        permissions = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not permissions.is_creator:
          return await event.answer("Only for chat creator")
        await event.edit("All pinned messages have been unpinned.", buttons=None)
        await tbot.unpin_message(event.chat_id)
