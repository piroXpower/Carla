from Carla import tbot
from telethon import events, Button
from Carla.events import Cbot
import os
try:
  from youtubesearchpython import SearchVideos
except ImportError:
  os.system('pip3 install youtube-search-python')
  from youtubesearchpython import SearchVideos
s = None

import urllib
@Cbot(pattern="^/suz")
async def _(event):
 global s
 k = await event.get_reply_message()
 m = await tbot.download_media(k, './', thumb=-1)
 s = m
 await event.respond('Done')


@tbot.on(events.InlineQuery(pattern=r"yt (.*)"))
async def inline_id_handler(event: events.InlineQuery.Event):
    builder = event.builder
    k = event.pattern_match.group(1)
    if ";" in k:
         testinput,bc = event.pattern_match.group(1).split(";")
    else:
         testinput = event.pattern_match.group(1)
         bc = 5
    urllib.parse.quote_plus(testinput)
    lund = event.sender_id
    if lund == lund:
        results = []
        search = SearchVideos(f"{testinput}", offset=1, mode="dict", max_results=int(bc))
        mi = search.result()
        moi = mi["search_result"]
        if search == None:
            resultm = builder.article(
                title="No Results.",
                description="Try Again With correct Spelling",
                text="**No Matching Found**",
                buttons=[
                    [Button.switch_inline("Search Again", query="yt ", same_peer=True)],
                ],
            )
            await event.answer([resultm])
            return
        for mio in moi:
            mo = mio["link"]
            thum = mio["title"]
            proboyx = mio["id"]
            thums = mio["channel"]
            td = mio["duration"]
            tw = mio["views"]
            kekme = f"https://img.youtube.com/vi/{proboyx}/hqdefault.jpg"
            okayz = f"**Title :** `{thum}` \n**Link :** Ruk \n**Channel :** `{thums}` \n**Views :** `{tw}` \n**Duration :** `{td}`"
            hmmkek = f"Channel : {thums} \nDuration : {td} \nViews : {tw}"
            results.append(
                await event.builder.article(
                    title=thum,
                    thumb=kekme,
                    description=hmmkek,
                    text=okayz,
                    buttons=Button.switch_inline(
                        "Search Again", query="yt ", same_peer=True
                    ),
                )
            )
        await event.answer(results)
