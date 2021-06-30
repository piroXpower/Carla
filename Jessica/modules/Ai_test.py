from Jessica.events import Cbot
from Jessica import ubot

@Cbot(pattern="^/test ?(*.)")
async def cb(e):
 q = event.pattern_match.group(1)
 if not q:
   return
 async with ubot.conversation("@KukiAI_bot") as chat:
   await chat.send_message(str(q))
   res = await chat.get_response()
   await res.forward_message(event.chat_id)
