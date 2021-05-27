from telethon.errors import PackShortNameOccupiedError
from telethon.tl.functions.stickers import CreateStickerSetRequest as create_set
from telethon.tl.types import InputDocument, InputStickerSetItem, MaskCoords

from Evelyn import tbot
from Evelyn.events import Cbot

from . import db

sticker_sets = db.sticker_sets


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
    if str((sticker_sets.find({"id": event.sender_id})).distinct("sticker_id")) == "[]":
       return await event.reply("SpCk")
    try:
        result = await tbot(
            create_set(
                user_id=user_id,
                title=f"{event.sender.first_name}'s Kang pack",
                short_name=f"e{event.sender_id}_by_MissCarla_Bot",
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
        sticker_sets.insert_one(
            {
                "id": event.sender_id,
                "sticker_id": result.set.id,
                "access_hash": result.set.access_hash,
            }
        )
    except PackShortNameOccupiedError:
        user_st = sticker_sets.find({"id": event.sender_id})
        sticker_id = user_st.distinct("sticker_id")[0]
        access_hash = user_st.distinct("access_hash")[0]
        await event.reply(f"ID:{sticker_id} HASH:{access_hash}")
    except Exception as e:
        return await event.respond(str(e))
    await event.respond(str(result)[:200])
