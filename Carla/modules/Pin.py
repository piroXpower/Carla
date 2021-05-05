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
    await can_pin_messages(event.chat_id, event.sender_id)
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
 if event.text.startswith("?pinned") or event.text.startswith("!pinned") or event.text.startswith("/pinned"):
  return
 if event.is_private:
  return #connect
 if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
    await can_pin_messages(event.chat_id, event.sender_id)
 if not event.reply_to_msg_id:
  msg = await tbot.get_messages(event.chat_id, ids=types.InputMessagePinned())
  id = msg.id
 else:
  reply = await event.get_reply_message()
  id = reply.message.id
 await event.reply(f"{id}")
