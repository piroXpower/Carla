from telethon import events, types

import Evelyn.modules.mongodb.notes_db as db
from Evelyn import tbot
from Evelyn.events import Cbot

from . import button_parser, can_change_info, get_reply_msg_btns_text


def file_ids(msg):
    if isinstance(msg.media, types.MessageMediaDocument):
        file_id = msg.media.document.id
        access_hash = msg.media.document.access_hash
        file_reference = msg.media.document.file_reference
        type = "doc"
    elif isinstance(msg.media, types.MessageMediaPhoto):
        file_id = msg.media.photo.id
        access_hash = msg.media.photo.access_hash
        file_reference = msg.media.photo.file_reference
        type = "photo"
    elif isinstance(msg.media, types.MessageMediaGeo):
        file_id = msg.media.geo.long
        access_hash = msg.media.geo.lat
        file_reference = msg.media.geo.access_hash
        type = "geo"
    else:
        return None, None, None, None
    return file_id, access_hash, file_reference, type


def id_tofile(file_id, access_hash, file_reference, type):
    if file_id == None:
        return None
    if type == "doc":
        return types.InputDocument(
            id=file_id, access_hash=access_hash, file_reference=file_reference
        )
    elif type == "photo":
        return types.Photo(
            id=file_id, access_hash=access_hash, file_reference=file_reference
        )
    elif type == "geo":
        return types.GeoPoint(
            long=file_id,
            lat=access_hash,
            access_hash=file_reference,
            accuracy_radius=None,
        )


@Cbot(pattern="^/save ?(.*)")
async def save(event):
    if event.is_private:
        return
    if event.from_id:
        file_id = access_hash = file_reference = type = None
        if event.is_group:
            if not await can_change_info(event, event.sender_id):
                return
        if not event.reply_to and not event.pattern_match.group(1):
            return await event.reply("You need to give the note a name!")
        elif event.reply_to:
            n = event.pattern_match.group(1)
            r_msg = await event.get_reply_message()
            if r_msg.media:
                file_id, access_hash, file_reference, type = file_ids(r_msg)
            if not r_msg.text and not r_msg.media:
                return await event.reply("you need to give the note some content!")
            if not n:
                return await event.reply("You need to give the note a name!")
            r_note = r_msg.text or "Nil"
            if r_msg.reply_markup:
                _buttons = get_reply_msg_btns_text(r_msg)
                r_note = r_msg.text + _buttons
        elif event.pattern_match.group(1):
            n = event.pattern_match.group(1)
            n = n.split(None, 1)
            if len(n) == 1:
                return await event.reply("you need to give the note some content!")
            n = n[0]
            r_note = n[1]
        db.save_note(
            event.chat_id, n, r_note, file_id, access_hash, file_reference, type
        )
        await event.reply(f"Saved note `{n}`")


@tbot.on(events.NewMessage(pattern=r"\#(\S+)"))
async def new_message_note(event):
    name = event.pattern_match.group(1)
    note = db.get_note(event.chat_id, name)
    if not note:
        return
    if note["note"] == "Nil":
        caption = None
    file = id_tofile(note["id"], note["hash"], note["ref"], note["mtype"])
    if caption:
        caption, buttons = button_parser(caption)
    else:
        buttons = None
    await event.respond(
        caption,
        file=file,
        buttons=buttons,
        parse_mode="md",
        reply_to=event.reply_to_msg_id or event.id,
    )
