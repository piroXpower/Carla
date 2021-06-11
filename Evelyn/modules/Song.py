from Evelyn import ubot
from Evelyn.events import Cbot


@Cbot(pattern="^/music ?(.*)")
async def music(event):
    music = event.pattern_match.group(1)
    if not music:
        return
    async with ubot.conversation("@EvelynMusic_Bot") as conv:
        await conv.send_message(music)
        res = await conv.get_response()
        if "Sorry" in res.raw_text:
            return await event.reply("Failed to find the song!")
        await res.click(0)
        await conv.get_response()
