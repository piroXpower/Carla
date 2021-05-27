from telethon.tl.functions.stickers import CreateStickerSetRequest as create_set
from telethon.tl.types import InputDocument, InputStickerSetItem, MaskCoords

from Evelyn import tbot
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
                emoji = msg.media.document.attributes[1].alt
            else:
                emoji = "😂"
    if event.pattern_match.group(1):
        emoji = event.pattern_match.group(1)[0]
    sticker_id = msg.media.document.id
    access_hash = msg.media.document.access_hash
    file_reference = msg.media.document.file_reference
    event.sender.first_name + "'s Kang pack"
    event.sender.first_name + "'s pack1"
    user_id = event.sender_id
    try:
        result = await tbot(
            create_set(
                user_id=user_id,
                title=f"a{event.sender_id}_by_MissCarla_Bot",
                short_name=f"a{event.sender_id}_by_MissCarla_Bot",
                stickers=[
                    InputStickerSetItem(
                        document=InputDocument(
                            id=sticker_id,
                            access_hash=access_hash,
                            file_reference=file_reference,
                        ),
                        emoji=emoji,
                        mask_coords=MaskCoords(n=42, x=7.13, y=7.13, zoom=7.13),
                    )
                ],
                masks=False,
                animated=False,
            )
        )
    except Exception as e:
        return await event.respond(str(e))
    await event.respond(str(result)[:200])
