import yt_dlp
from pytgcalls import GroupCallFactory

from .. import ubot
from ..utils import Cbot

ops = {"quiet": True}
from youtubesearchpython import VideosSearch as vs

from .. import OWNER_ID
from . import DEVS

p = DEVS
p.append(OWNER_ID)

db = {}


@Cbot(pattern="^/playvideo ?(.*)")
async def play_video(e):
    try:
        global p
        if not e.sender_id in p:
            return
        try:
            q = e.text.split(None, 1)[1]
        except IndexError:
            return await e.reply("No Query.")
        if not q.startswith("https"):
            try:
                v = vs(q, limit=1).result()["result"][0]
            except (IndexError, KeyError, TypeError):
                return await e.reply("No song result found for your query!")
            q = v["link"]
        with yt_dlp.YoutubeDL(ops) as yt:
            yts = yt.extract_info(q, download=False)
        aud = yts.get("formats")[1].get("url")
        vid = yts.get("formats")[-1].get("url")
        if not aud:
            return await e.reply("No Search Result Found for Your Query.")
        await e.reply("Playing **{}** by {}".format(yts.get("title")))
        if not db.get(e.chat_id):
            call = GroupCallFactory(
                ubot, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON
            ).get_group_call()
        else:
            call = db.get(e.chat_id)
            await call.stop()
            await call.join(e.chat_id)
            await call.start_audio(aud, repeat=False)
            return await call.start_video(vid, repeat=False, with_audio=False)
        await call.join(e.chat_id)
        await call.start_video(vid, repeat=False, with_audio=False)
        await call.start_audio(aud, repeat=False)
        db[e.chat_id] = call
    except Exception as ep:
        await e.reply(str(ep))
