from telethon import Button, events, types
from Carla import tbot, BOT_ID, OWNER_ID
from . import is_admin, can_pin_messages, ELITES
from Carla.events import Cbot

@Cbot(pattern="^/pinned")
async def _(event):
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
