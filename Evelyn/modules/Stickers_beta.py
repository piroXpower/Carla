import os

from Evelyn.events import Cbot


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
                msg.media.document.attributes[1].alt
            else:
                pass
    if event.pattern_match.group(1):
        event.pattern_match.group(1)[0]
    sticker = await tbot.download_media(msg.media)
    await event.reply(file=sticker)
    os.remove(sticker)
