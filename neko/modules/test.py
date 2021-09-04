from pytgcalls import GroupCallFactory
import youtube_dl
from .. import ubot
from ..utils import Cbot
ops = {"quiet": True}
from .. import OWNER_ID
from . import DEVS
p = DEVS
p.append(OWNER_ID)


@Cbot(pattern="^/video ?(.*)")
async def play_video(e):
 global p
 if not e.sender_id in p:
   return
 try:
   q = e.text.split(None, 1)[1]
 except IndexError:
   return await e.reply("No Query.")
 with youtube_dl.YoutubeDL(ops) as yt:
   yts = yt.extract_info(q, download=False)
 url = yts.get('formats')[0].get('url')
 if not url:
   return await e.reply("No Search Result Found for Your Query.")
 call = GroupCallFactory (ubot, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON).get_group_call()
 await call.join(e.chat_id)
 await call.start_video(url, repeat=True)
