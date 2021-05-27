from Evelyn.events import Cbot
from Evelyn import ybot
import os


@Cbot(pattern="^/kang ?(.*)")
async def kang(event):
    if not event.reply_to_msg_id:
        return
    msg = await event.get_reply_message()
    if not msg.sticker:
        return await event.reply("I can't kang that.")
    if msg.media:
        if msg.media.document:
            if msg.media.document.attributes:
                emoji = msg.media.document.attributes[1].alt
            else:
                emoji = "😂"
    if event.pattern_match.group(1):
        emoji = event.pattern_match.group(1)[0]
    sticker = await tbot.download_media(msg.media)
    await event.reply(file=sticker)
    os.remove(sticker)
