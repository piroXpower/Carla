from .. import pbot
from pytgcalls import GroupCall

@Cbot(pattern="^/joinvc")
async def query_pytgcalls(e):
 chat_id = e.chat_id
 await GroupCall(pbot).start(chat_id)
 await e.reply("Joined VC")
