import os
from . import runcmd
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
    search = VideosSearch(q, limit=1)
    if not search:
        return await event.reply(f"Song Not Found With Name {q}.")
    r = (search.result())["result"]
    url = r[0]["url"]
    x_u = await st_r.edit(f"`Preparing to upload song:` **{str(r[0]['title'])}**")
    await runcmd("yt-dlp {} -x --audio-quality 0 -o "~/YouTube/%(id)s.%(ext)s" -q --default-search ytsearch --no-cache-dir --geo-bypass -title".format(url))
    du_s = (str(r[0]["duration"])).split(":", 1)
    du = (int(du_s[0]) * 60) + int(du_s[1])
    fil_e = f'/root/YouTube/{r[0]["id"]}.opus'
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
