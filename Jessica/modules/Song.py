from Jessica import tbot
from Jessica.events import Cbot
import youtube_dl
import os
from youtubesearchpython import SearchVideos


@Cbot(pattern="^/song ?(.*)")
async def song(event):
 q = event.pattern_match.group(1)
 if not q:
   return await event.reply("Please provide the name of the song!")
 ydl_opts = {
    'format': 'bestaudio/best',
   'outtmpl': 'y_dl.mp3',
   'quiet': True,
}
 search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
 if not search:
   return await event.reply(f"Song Not Found With Name {input_str}."
        )
 r = search.result()
 title = r[0]["title"]
 with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([f'ytsearch:{q}'])
 await event.reply(str(title), file="y_dl.mp3")
 or.remove("y_dl.mp3")
 
