from Evelyn import tbot
from Evelyn.events import Cbot

@Cbot(pattern="^/kang ?(.*)")
async def kang(event):
 if not event.reply_to_msg_id:
   return
 msg = await event.get_reply_message()
 if not msg.media:
   return await event.reply("I can't kang that.")
 if msg.media:
   if msg.media.document:
     if msg.media.document.attributes:
       emoji = msg.media.document.attributes[1].alt
     else:
       emoji = "😂"
 if event.pattern_match.group(1):
   emoji = event.pattern_match.group(1)[0]
 await event.respond(str(emoji))
