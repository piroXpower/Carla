import re

from telethon import events, types

import Jessica.modules.mongodb.filters_db as db
from Jessica import tbot
from Jessica.events import Cbot

from . import can_change_info, get_reply_msg_btns_text


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
        file_reference = None
        type = "geo"
    else:
        return None, None, None, None
    return file_id, access_hash, file_reference, type


@Cbot(pattern="^/filter ?(.*)")
async def add_filter(event):
    if (
        event.text.startswith("!filters")
        or event.text.startswith("/filters")
        or event.text.startswith("?filters")
        or event.text.startswith(".filters")
    ):
        return
    if event.from_id:
        if not isinstance(event.from_id, types.PeerUser):
            return
    if event.is_group and event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    file_id = file_reference = access_hash = type = None
    if not event.reply_to and not event.pattern_match.group(1):
        return await event.reply("You need to give the filter a name!")
    elif event.reply_to:
        name = event.pattern_match.group(1)
        if not name:
            return await event.reply("You need to give the filter a name!")
        reply_msg = await event.get_reply_message()
        if reply_msg.media:
            file_id, access_hash, file_reference, type = file_ids(reply_msg)
        if not reply_msg.text and not reply_msg.media:
            return await event.reply("you need to give the filter some content!")
        reply = reply_msg.text or "Nil"
        if reply_msg.reply_markup:
            reply = reply + get_reply_msg_btns_text(reply_msg)
    elif event.pattern_match.group(1):
        _total = event.text.split(None, 1)[1]
        _t = _total.split(None, 1)
        if len(_t) == 1:
            return await event.reply("You need to give the filter some content!")
        name = _t[0]
        reply = _t[1]
    await event.reply("Saved filter '{}'.".format(name))
    db.save_filter(
        event.chat_id, name, reply, file_id, access_hash, file_reference, type
    )


@tbot.on(events.NewMessage())
async def filter_trigger(event):
    name = event.text
    snips = db.get_all_filters(event.chat_id)
    if not snips:
        return
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            filter = db.get_filter(event.chat_id, snip)
            print(filter)
