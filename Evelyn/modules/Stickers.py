import math

from PIL import Image
from telethon.errors.rpcerrorlist import StickerEmojiInvalidError, StickerPngNopngError
from telethon.tl.functions.stickers import (
    AddStickerToSetRequest,
    CreateStickerSetRequest,
    RemoveStickerFromSetRequest,
)
from telethon.tl.types import (
    InputDocument,
    InputStickerSetID,
    InputStickerSetItem,
    MaskCoords,
    MessageMediaPhoto,
)

from Evelyn import OWNER_ID, tbot
from Evelyn.events import Cbot

from . import db

sticker_sets = db.sticker_packs


@Cbot(pattern="^/(kang|kamg) ?(.*)")
async def kang(event):
    try:
        if not event.reply_to_msg_id:
            return await event.reply("Please reply to a sticker, or image to kang it!")
        msg = await event.get_reply_message()
        if not msg.sticker and not isinstance(msg.media, MessageMediaPhoto):
            return await event.reply("Yeah, I can't kang that.")
        try:
            emoji = msg.media.document.attributes[1].alt
        except:
            emoji = "😂"
        if event.pattern_match.group(2):
            emoji = event.pattern_match.group(2)[0]
        if msg.sticker:
            mime_type = msg.media.document.mime_type
            if "application/x-tgsticker" in mime_type:
                return
            sticker_id_id = msg.media.document.id
            access_hash_id = msg.media.document.access_hash
            file_reference = msg.media.document.file_reference
        elif msg.media.photo:
            file = await tbot.download_media(msg)
            resize_image(file)
            sended = await tbot.send_message("RoseLoverZ", file="sticker.webp")
            sticker_id_id = sended.media.document.id
            access_hash_id = sended.media.document.access_hash
            file_reference = sended.media.document.file_reference
            os.remove("sticker.webp")
            await sended.delete()
        short_name = f"ev{event.sender_id}_by_MissEvelyn_Bot"
        user_id = OWNER_ID
        if event.sender.first_name:
            title = f"{event.sender.first_name}'s Kang pack"
        else:
            title = f"{event.sender_id}'s Kang pack"
        if (
            str((sticker_sets.find({"id": event.sender_id})).distinct("sticker_id"))
            == "[]"
        ):
            try:
                result = await tbot(
                    CreateStickerSetRequest(
                        user_id=user_id,
                        title=title,
                        short_name=short_name,
                        stickers=[
                            InputStickerSetItem(
                                document=InputDocument(
                                    id=sticker_id_id,
                                    access_hash=access_hash_id,
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
            except StickerPngNopngError:
                return
            except StickerEmojiInvalidError:
                return await event.reply(
                    f"Invalid emoji provided, '{event.pattern_match.group(1)}' is not an emoji."
                )
            except Exception as e:
                return await event.reply(str(e))
            txt = f"Sticker successfully added to <a href='http://t.me/addstickers/{short_name}'>pack</a>\nEmoji is: {emoji}"
            await event.reply(txt, parse_mode="html", link_preview=False)
            return sticker_sets.insert_one(
                {
                    "id": event.sender_id,
                    "sticker_id": result.set.id,
                    "access_hash": result.set.access_hash,
                }
            )
        user_st = sticker_sets.find({"id": event.sender_id})
        sticker_id = user_st.distinct("sticker_id")[0]
        access_hash = user_st.distinct("access_hash")[0]
        try:
            result = await tbot(
                AddStickerToSetRequest(
                    stickerset=InputStickerSetID(
                        id=sticker_id, access_hash=access_hash
                    ),
                    sticker=InputStickerSetItem(
                        document=InputDocument(
                            id=sticker_id_id,
                            access_hash=access_hash_id,
                            file_reference=file_reference,
                        ),
                        emoji=emoji,
                    ),
                )
            )
        except StickerPngNopngError:
            return
        except StickerEmojiInvalidError:
            return await event.reply(
                f"Invalid emoji provided, '{event.pattern_match.group(1)}' is not an emoji."
            )
        except Exception as e:
            return await event.respond(str(e))
        txt = f"Sticker successfully added to <a href='http://t.me/addstickers/{result.set.short_name}'>pack</a>\nEmoji is: {emoji}"
        await event.reply(txt, parse_mode="html", link_preview=False)
    except Exception as e:
        await event.reply(str(e))


# work on animated sticker


@Cbot(pattern="^/(rmkang|unkang)$")
async def uk(event):
    if not event.reply_to_msg_id:
        return
    msg = await event.get_reply_message()
    if not msg.sticker:
        return await event.reply("Yeah, that's not a sticker!")
    sticker_id = msg.media.document.id
    access_hash = msg.media.document.access_hash
    file_reference = msg.media.document.file_reference
    try:
        result = await tbot(
            RemoveStickerFromSetRequest(
                sticker=InputDocument(
                    id=sticker_id,
                    access_hash=access_hash,
                    file_reference=file_reference,
                ),
            )
        )
        await event.reply(
            f"Sticker sucessfully removed from <a href='http://t.me/addstickers/{result.set.short_name}'>pack</a>",
            parse_mode="HTML",
        )
    except:
        await event.reply(
            "The provided sticker set is invalid or sticker pack not made by me!"
        )


def resize_image(image):
    im = Image.open(image)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    os.remove(file)
    im.save("sticker.webp")


async def animated_sticker_kang(event, msg):
    print("ani kang")
