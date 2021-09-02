import os
import random

import emoji
from bs4 import BeautifulSoup
from requests import get
from telethon import Button
from telethon.errors.rpcerrorlist import (
    PackShortNameOccupiedError,
    StickerEmojiInvalidError,
    StickerPngNopngError,
)
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.stickers import (
    AddStickerToSetRequest,
    CreateStickerSetRequest,
    RemoveStickerFromSetRequest,
)
from telethon.tl.types import (
    DocumentAttributeSticker,
    InputDocument,
    InputStickerSetEmpty,
    InputStickerSetID,
    InputStickerSetItem,
    MaskCoords,
    MessageMediaPhoto,
)

from .. import CMD_HELP, OWNER_ID, tbot
from ..events import Cbot
from . import db, resize_image

sticker_sets = db.sticker_packs
pkang = db.pack_kang


def get_emoji(v):
    p = "".join(c for c in v if c in emoji.UNICODE_EMOJI["en"])
    if len(p) != 0:
        return p[0]
    return None


@Cbot(pattern="^/kang(@MissNeko_Bot)? ?(.*)")
async def kang(event):
    if not event.reply_to:
        return await event.reply("Please reply to a sticker, or image to kang it!")
    if not event.from_id:
        return await e.reply("You are an anon admin, kang in my PM!")
    msg = await event.get_reply_message()
    if not (
        msg.sticker or (msg.document and "image" not in msg.document.mime_type)
    ) and not isinstance(msg.media, MessageMediaPhoto):
        return await event.reply("Yeah, I can't kang that.")
    try:
        emoji = event.text.split(None, 1)[1]
        emoji = get_emoji(emoji) or ""
    except IndexError:
        try:
            emoji = msg.media.document.attributes[1].alt
        except:
            emoji = "😂"
    if emoji == "":
        emoji = random.choice(["😍", "😂", "🙅‍♀️"])
    if msg.sticker:
        mime_type = msg.media.document.mime_type
        if "application/x-tgsticker" in mime_type:
            return await e.reply("Kanging animated stickers is not supported yet!")
        sticker_id_id = msg.media.document.id
        access_hash_id = msg.media.document.access_hash
        file_reference = msg.media.document.file_reference
    elif msg.media.photo:
        file = await tbot.download_media(msg)
        resize_image(file)
        sended = await tbot.send_message("RoseLoverX", file="sticker.webp")
        sticker_id_id = sended.media.document.id
        access_hash_id = sended.media.document.access_hash
        file_reference = sended.media.document.file_reference
        os.remove("sticker.webp")
        await sended.delete()
    short_name = f"nk{event.sender_id}_by_MissNeko_Bot"
    user_id = OWNER_ID
    if event.sender.first_name:
        title = f"{event.sender.first_name}'s Kang pack"
    else:
        title = f"{event.sender_id}'s Kang pack"
    if str((sticker_sets.find({"id": event.sender_id})).distinct("sticker_id")) == "[]":
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
                stickerset=InputStickerSetID(id=sticker_id, access_hash=access_hash),
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
        return await event.reply(str(e))
    txt = f"Sticker successfully added to <b><a href='http://t.me/addstickers/{result.set.short_name}'>Pack</a></b>\nEmoji is: {emoji}"
    await event.reply(
        txt,
        parse_mode="html",
        link_preview=False,
        buttons=Button.url(
            "View Pack", f"http://t.me/addstickers/{result.set.short_name}"
        ),
    )


@Cbot(pattern="^/unkang(@MissNeko_Bot)?$")
async def unkang__own_sticker(e):
    if not e.reply_to_msg_id:
        return await e.reply("Reply to a sticker from your stickerset to Unkang It!")
    r = await e.get_reply_message()
    if not r.sticker:
        return await e.reply("Yeah, that's not a sticker to unkang!")
    sticker_id = r.media.document.id
    access_hash = r.media.document.access_hash
    file_reference = r.media.document.file_reference
    pack_id = None
    for x in r.document.attributes:
        if isinstance(x, DocumentAttributeSticker):
            if x.stickerset:
                pack_id = x.stickerset.id
    if not pack_id:
        return await e.reply(
            "That sticker doesn't belong to any pack, then what's the point of unkanging it?"
        )
    if e.sender_id != OWNER_ID:
        px = sticker_sets.find_one({"sticker_id": pack_id})
        if px == None or px.get("id") != e.sender_id:
            return await e.reply("That Sticker pack is not yours to Unkang!")
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
        await e.reply(
            f"Sticker sucessfully removed from <b><a href='http://t.me/addstickers/{result.set.short_name}'>Pack</a></b>",
            parse_mode="HTML",
            buttons=Button.url(
                "View Pack", f"http://t.me/addstickers/{result.set.short_name}"
            ),
        )
    except:
        await e.reply(
            "The provided sticker set is invalid or the sticker pack is not made by me!"
        )


@Cbot(pattern="^/mypac(k|ks)(@MissNeko_Bot)? ?(.*)")
async def my_pack(e):
    if str((sticker_sets.find({"id": e.sender_id})).distinct("sticker_id")) == "[]":
        return await e.reply("You have not yet created any sticker packs!")
    user_st = sticker_sets.find({"id": e.sender_id})
    sticker_id = user_st.distinct("sticker_id")[0]
    access_hash = user_st.distinct("access_hash")[0]
    x = await tbot(
        GetStickerSetRequest(
            stickerset=InputStickerSetID(id=sticker_id, access_hash=access_hash)
        )
    )
    short_name = x.set.short_name
    await e.reply(
        f'Here is your kang <a href="http://t.me/addstickers/{short_name}">Pack</a>.',
        parse_mode="html",
        link_preview=False,
    )


@Cbot(pattern="^/(pkang|packkang)(@MissNeko_Bot)? ?(.*)")
async def pck_kang__(e):
    if not e.reply_to:
        return await e.reply("Reply to a sticker.")
    r = await e.get_reply_message()
    if not r.sticker:
        return await e.reply("That's not a sticker file.")
    if len(e.text.split(" ", 1)) == 2:
        pname = e.text.split(" ", 1)[1]
        emoji = get_emoji(pname)
        if emoji:
            if pname.startswith(emoji):
                emoji = None
            else:
                pname = pname.replace(emoji, "")
    else:
        pname = f"{e.sender.first_name}'s PKang pack"
        emoji = None
    id = access_hash = None
    for x in r.sticker.attributes:
        if isinstance(x, DocumentAttributeSticker):
            if not isinstance(x.stickerset, InputStickerSetEmpty):
                id = x.stickerset.id
                access_hash = x.stickerset.access_hash
    if not (id or access_hash):
        return await e.reply("That sticker is not part of any pack to kang!")
    _stickers = await tbot(
        GetStickerSetRequest(
            stickerset=InputStickerSetID(id=id, access_hash=access_hash)
        )
    )
    stk = []
    if emoji:
        for x in _stickers.documents:
            stk.append(
                InputStickerSetItem(
                    document=InputDocument(
                        id=x.id,
                        access_hash=x.access_hash,
                        file_reference=x.file_reference,
                    ),
                    emoji=emoji,
                )
            )
    else:
        for x in _stickers.documents:
            stk.append(
                InputStickerSetItem(
                    document=InputDocument(
                        id=x.id,
                        access_hash=x.access_hash,
                        file_reference=x.file_reference,
                    ),
                    emoji=(x.attributes[1]).alt,
                )
            )
    pack = 1
    xp = pkang.find_one({"user_id": e.sender_id})
    if xp:
        pack = xp.get("pack") + 1
    pkang.update_one({"user_id": e.sender_id}, {"$set": {"pack": pack}}, upsert=True)
    pm = random.choice(["a", "b", "c", "d", "e", "f", "g"])
    try:
        p = await tbot(
            CreateStickerSetRequest(
                user_id=e.sender_id,
                title=pname,
                short_name=f"{pm}{e.sender_id}_{pack}_by_MissNeko_Bot",
                stickers=stk,
            )
        )
    except PackShortNameOccupiedError:
        pack += 1
        p = await tbot(
            CreateStickerSetRequest(
                user_id=e.sender_id,
                title=pname + f"Vol {pack}",
                short_name=f"{pm}{e.sender_id}_{pack}_by_MissNeko_Bot",
                stickers=stk,
            )
        )
    except Exception as ex:
        return await e.reply(str(ex))
    await e.reply(
        f"Sticker Set successfully Kanged to <b><a href='http://t.me/addstickers/{p.set.short_name}'>Pack</a></b>.",
        buttons=Button.url(
            "View Pack", url=f"http://t.me/addstickers/{p.set.short_name}"
        ),
        parse_mode="html",
    )


@Cbot(pattern="^/stickers(@MissNeko_Bot)? ?(.*)")
async def search_combot_stickers__(e):
    if len(e.text.split(" ", 1)) == 2:
        q = e.text.split(" ", 1)[1]
    else:
        return await e.reply("Provide Some Name To Search For Packs.")
    url = "https://combot.org/telegram/stickers?q={}".format(q)
    r = get(url)
    if not r.ok:
        return
    soup = BeautifulSoup(r.content, "html.parser")
    results = soup.find_all("a", {"class": "sticker-pack__btn"})
    if not results:
        return await e.reply("No results found :(.")
    titles = soup.find_all("div", "sticker-pack__title")
    text = "Stickers for **{}**".format(q)
    Q = 1
    for x, y in zip(results, titles):
        if Q == 7:
            break
        Q += 1
        text += "\n• [{}]({})".format(y.get_text(), x["href"])
    await e.reply(text)


__name__ = "stickers"
__help__ = """
Here is the help for **Stickers** module:

-> /kang
Kang a sticker to your pack.
-> /unkang 
Remove a sticker from your pack.
-> /mypacks
List your kang packs.
-> /pkang <pack name(optional)>
Kang the replied sticker pack.
-> /stickers <query>
Search for global sticker packs.
"""
CMD_HELP.update({__name__: [__name__, __help__]})
