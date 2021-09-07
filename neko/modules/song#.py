import os

import yt_dlp
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from youtubesearchpython import VideosSearch as vs

from ..utils import Cbot

aud_ops = {
    "format": "bestaudio",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }
    ],
    "outtmpl": "%(id)s.mp3",
    "quiet": True,
    "logtostderr": False,
}
vid_ops = {
    "format": "best[height<=480]",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
    "outtmpl": "%(id)s.mp4",
    "logtostderr": False,
    "quiet": True,
}


@Cbot(pattern="^/song ?(.*)")
async def download_song(e):
    try:
        q = e.text.split(None, 1)[1]
    except IndexError:
        return await e.reply("The song query was not provided!")
    try:
        v = vs(q, limit=1).result()["result"][0]
    except (IndexError, KeyError, TypeError):
        return await e.reply("No song result found for your query!")
    axe = await e.reply(
        "Preparing to upload **{}** by {}".format(
            v.get("title"), v.get("channel").get("name") or "Channel"
        )
    )
    duration = int(v["duration"].split(":")[0]) * 60 + int(v["duration"].split(":")[1])
    if duration > 3600:
        await axe.edit("Upload failed song duration is more than 1 hour!")
    with yt_dlp.YoutubeDL(aud_ops) as yt:
        try:
            yt.extract_info(v["link"])
        except Exception as bx:
            return await axe.edit(str(bx))
    await e.client.send_file(
        e.chat_id,
        v["id"] + ".mp3",
        supports_streaming=False,
        force_document=False,
        allow_cache=False,
        attributes=[
            DocumentAttributeAudio(
                duration=duration, title=v["title"], performer=v["channel"]["name"]
            )
        ],
    )
    await axe.delete()
    os.remove(v["id"] + ".mp3")


@Cbot(pattern="^/video ?(.*)")
async def download_video(e):
    try:
        q = e.text.split(None, 1)[1]
    except IndexError:
        return await e.reply("The video query was not provided!")
    try:
        v = vs(q, limit=1).result()["result"][0]
    except (IndexError, KeyError, TypeError):
        return await e.reply("No video result found for your query!")
    axe = await e.reply(
        "Preparing to upload Video **{}** by {}".format(
            v.get("title"), v.get("channel").get("name") or "Channel"
        )
    )
    duration = int(v["duration"].split(":")[0]) * 60 + int(v["duration"].split(":")[1])
    with yt_dlp.YoutubeDL(vid_ops) as yt:
        try:
            yt.extract_info(v["link"])
        except Exception as bx:
            return await axe.edit(str(bx))
    await e.client.send_file(
        e.chat_id,
        v["id"] + ".mp4",
        supports_streaming=True,
        caption=v["title"],
        attributes=[DocumentAttributeVideo(duration=duration, w=1280, h=720)],
    )
    os.remove(v["id"] + ".mp4")
