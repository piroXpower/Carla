import datetime
import re

from telethon import events, types

from .. import BOT_ID, CMD_HELP, tbot
from ..events import Cbot, Cinline
from . import (
    button_parser,
    can_change_info,
    cb_is_owner,
    format_fill,
    get_reply_msg_btns_text,
    is_owner,
)
from .mongodb import filters_db as db


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


def id_tofile(file_id, access_hash, file_reference, type):
    if file_id == None:
        return None
    if type == "doc":
        return types.InputDocument(
            id=file_id, access_hash=access_hash, file_reference=file_reference
        )
    elif type == "photo":
        return types.Photo(
            id=file_id,
            access_hash=access_hash,
            file_reference=file_reference,
            date=datetime.datetime.now(),
            dc_id=5,
            sizes=[7108],
        )
    elif type == "geo":
        geo_file = types.InputMediaGeoPoint(
            types.InputGeoPoint(float(file_id), float(access_hash))
        )
        return geo_file


@Cbot(pattern="^/filter ?(.*)")
async def add_filter(event):
    if (
        event.text.startswith("!filters")
        or event.text.startswith("/filters")
        or event.text.startswith("?filters")
        or event.text.startswith("+filters")
    ):
        return
    if event.from_id:
        if not isinstance(event.from_id, types.PeerUser):
            return
    if event.is_group and event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    file_id = file_reference = access_hash = type = None
    try:
        f_text = event.text.split(None, 1)[1]
    except IndexError:
        f_text = None
    if not event.reply_to and not f_text:
        return await event.reply("You need to give the filter a name!")
    elif event.reply_to:
        name = f_text
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
    elif f_text:
        _total = f_text
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
    if event.sender_id == int(BOT_ID):
        return
    if (
        event.text.startswith("/filter")
        or event.text.startswith("!filter")
        or event.text.startswith("?filter")
        or event.text.startswith("+filter")
        or event.text.startswith("!stop")
        or event.text.startswith("?stop")
        or event.text.startswith("+stop")
        or event.text.startswith("/stop")
    ):
        return
    name = event.text
    snips = db.get_all_filters(event.chat_id)
    if not snips:
        return
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            filter = snips[snip]
            file = id_tofile(
                filter["id"], filter["hash"], filter["ref"], filter["mtype"]
            )
            caption = buttons = None
            if filter["reply"] and filter["reply"] != "Nil":
                caption, buttons = button_parser(filter["reply"])
            link_prev = False
            if caption and "{preview}" in caption:
                caption = caption.replace("{preview}")
                link_prev = True
            if caption:
                caption = await format_fill(event, caption)
            await event.respond(
                caption,
                file=file,
                buttons=buttons,
                link_preview=link_prev,
                reply_to=event.id,
            )


@Cbot(pattern="^/filters")
async def filter(event):
    if event.is_private:
        return
    snips = db.get_all_filters(event.chat_id)
    if snips:
        text = "<b>Filters in {}:</b>".format(event.chat.title)
        for snip in snips:
            text += "\n- <code>{}</code>".format(snip)
        await event.reply(text, parse_mode="html")
    else:
        await event.reply(f"No filters in {event.chat.title}!")


@Cbot(pattern="^/stop ?(.*)")
async def estop(event):
    if (
        event.text.startswith("+stopall")
        or event.text.startswith("/stopall")
        or event.text.startswith("?stopall")
        or event.text.startswith("!stopall")
    ):
        return
    try:
        name = event.text.split(None, 1)[1]
    except IndexError:
        name = None
    if not name:
        return await event.reply("Not enough arguments provided.")
    f_exist = db.get_filter(event.chat_id, name)
    if f_exist:
        await event.reply("Filter `'{}'` has been stopped!".format(name))
        return db.delete_filter(event.chat_id, name)
    await event.reply("You haven't saved any filters on this word yet!")


@Cbot(pattern="^/stopall")
async def delallfilters(event):
    if event.is_private:
        return
    if event.is_group:
        if event.from_id:
            if not await is_owner(event, event.sender_id):
                return
    buttons = [
        [Button.inline("Delete all filters", data="stopall")],
        [Button.inline("Cancel", data="cancelstopall")],
    ]
    text = f"Are you sure you would like to stop **ALL** filters in {event.chat.title}? This action cannot be undone."
    await event.reply(text, buttons=buttons)


@Cinline(pattern="stopall")
async def stopallcb(event):
    if not await cb_is_owner(event, event.sender_id):
        return
    await event.edit("Deleted all chat filters.", buttons=None)
    db.delete_all_filters(event.chat_id)


@Cinline(pattern="cancelstopall")
async def stopallcb(event):
    if not await cb_is_owner(event, event.sender_id):
        return
    await event.edit("Stopping of all filters has been cancelled.", buttons=None)


__name__ = "filters"
__help__ = """
Here is the help for **Filters** module:

**Admin Commands:**
-> /filter `<keyword> <reply/content>`
Everytime someone says "keyword" bot replies "content".
-> /stop `<keyword>`
Stop the bot from replying to "keyword".
-> /stopall
Stop all filters of a chat.

-> /filters
List the active filters of a chat.

**Examples:**
- Set filter
-> `/filter Hi Hello!`
- Set filter for admins
-> `/filter Hi Hello! {admin}`
- set file/image/geo/gif/sticker etc. As filter
-> `/filter <keyword> <reply to media>`
"""
CMD_HELP.update({__name__: [__name__, __help__]})
