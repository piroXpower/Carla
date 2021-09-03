import os

import youtube_dl
from telethon.tl.types import DocumentAttributeAudio
from youtubesearchpython import VideosSearch

from ..utils import Cbot


@Cbot(pattern="^/song ?(.*)")
async def song(event):
    q = event.pattern_match.group(1)
    if not q:
        return await event.reply("Please provide the name of the song!")
    st_r = await event.reply("`Processing...`")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
    }
    search = VideosSearch(q, limit=1)
    if not search:
        return await event.reply(f"Song Not Found With Name {q}.")
    r = (search.result())["result"]
    x_u = await st_r.edit(f"`Preparing to upload song:` **{str(r[0]['title'])}**")
    try:
        youtube_dl.YoutubeDL(ydl_opts).download([f"ytsearch:{q}"])
    except BaseException as bse:
        return await x_u.edit(str(bse))
    du_s = (str(r[0]["duration"])).split(":", 1)
    du = (int(du_s[0]) * 60) + int(du_s[1])
    fil_e = f'{r[0]["id"]}.mp3'
    await event.respond(
        file=fil_e,
        attributes=[
            DocumentAttributeAudio(
                duration=int(du),
                title=str(r[0]["title"]),
                performer="YouTube",
                waveform="320",
            )
        ],
    )
    await x_u.delete()
    os.remove(fil_e)
