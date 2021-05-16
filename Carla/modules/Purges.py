from Carla import thot
from Carla.events import Cbot
from . import can_del_msg, db
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
import asyncio


purgex = db.purge
def get_id(id):
    return purgex.find_one({"id": id})

@Cbot(pattern="^/purge ?(.*)")
async def pugre(event):
 lt = event.pattern_match.group(1)
 if lt:
   if not lt.isdigit():
      lt = None
 if lt:
   limit = lt
 else:
   limit = 500
 if event.is_group:
   if not await can_del_msg(event, event.sender_id):
       return
 if not event.reply_to_msg_id:
  return await event.reply("Reply to a message to show me where to purge from.")
 reply_msg = await event.get_reply_message()
 messages = []
 message_id = reply_msg.id
 delete_to = event.message.id
 messages.append(event.reply_to_msg_id)
 for msg_id in range(message_id, delete_to + 1):
   messages.append(msg_id)
   if len(messages) == limit:
       break
 try:
   await tbot.delete_messages(event.chat_id, messages)
 except MessageDeleteForbiddenError:
   return await event.reply("I can't delete messages that are too old!")
 x = await event.respond("Purge complete!")
 await asyncio.sleep(4)
 await x.delete()


