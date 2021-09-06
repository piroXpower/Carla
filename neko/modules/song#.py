import yt_dlp

from ..utils import Cbot

opts = {
    "format": "bestaudio",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "writethumbnail": True,
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


@Cbot(pattern="^/song ?(.*)")
async def song(e):
    try:
        e.text.split(None, 1)[1]
    except IndexError:
        return await e.reply("The song query was not provided!")
    with yt_dlp.YoutubeDL(ops) as yt:
        print(yt)
