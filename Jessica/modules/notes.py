import datetime

from telethon import Button, events, types

import Jessica.modules.mongodb.notes_db as db
from Jessica import tbot
from Jessica.events import Cbot, Cinline

from . import (
    button_parser,
    can_change_info,
    cb_is_owner,
    get_reply_msg_btns_text,
    is_admin,
    is_owner,
    format_fill,
)


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
            sizes=[718118],
        )
    elif type == "geo":
        geo_file = types.InputMediaGeoPoint(
            types.InputGeoPoint(float(file_id), float(access_hash))
        )
        return geo_file


@Cbot(pattern="^/save ?(.*)")
async def save(event):
    if (
        event.text.startswith("+saved")
        or event.text.startswith("/saved")
        or event.text.startswith("?saved")
        or event.text.startswith("!saved")
    ):
        return
    if event.from_id:
        file_id = access_hash = file_reference = type = None
        if event.is_group:
            if not await can_change_info(event, event.sender_id):
                return
        try:
            f_text = event.text.split(None, 1)[1]
        except IndexError:
            f_text = None
        if not event.reply_to and not f_text:
            return await event.reply("You need to give the note a name!")
        elif event.reply_to:
            xp = f_text.split(None, 1)
            n = xp[0]
            r_msg = await event.get_reply_message()
            if r_msg.media:
                file_id, access_hash, file_reference, type = file_ids(r_msg)
            if not r_msg.text and not r_msg.media:
                return await event.reply("you need to give the note some content!")
            if not n:
                return await event.reply("You need to give the note a name!")
            note = r_msg.text or ""
            if len(xp) == 2:
                note = xp[1]
            if r_msg.reply_markup:
                _buttons = get_reply_msg_btns_text(r_msg)
                note = r_msg.text + _buttons
            x = [n, note]
        elif f_text:
            n = f_text or "x"
            x = n.split(" ", 1)
            if len(x) == 1:
                return await event.reply("you need to give the note some content!")
        db.save_note(
            event.chat_id, x[0], x[1], file_id, access_hash, file_reference, type
        )
        await event.reply(f"Saved note `{x[0]}`")


@Cbot(pattern="^/privatenotes ?(.*)")
async def pnotes(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return  # for now
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    arg = event.pattern_match.group(1)
    if not arg:
        mode = db.get_pnotes(event.chat_id)
        if mode:
            await event.reply(
                "Your notes are currently being sent in private. Jessica will send a small note with a button which redirects to a private chat."
            )
        else:
            await event.reply("Your notes are currently being sent in the group.")
    elif arg in ["y", "yes", "on"]:
        await event.reply(
            "Jessica will now send a message to your chat with a button redirecting to PM, where the user will receive the note."
        )
        db.change_pnotes(event.chat_id, True)
    elif arg in ["n", "no", "off"]:
        await event.reply("Jessica will now send notes straight to the group.")
        db.change_pnotes(event.chat_id, False)
    else:
        await event.reply(
            f"failed to get boolean value from input: expected one of y/yes/on or n/no/off; got: {arg}"
        )


@tbot.on(events.NewMessage(pattern=r"\#(\S+)"))
async def new_message_note(event):
    name = event.pattern_match.group(1)
    note = db.get_note(event.chat_id, name)
    if not note:
        return
    p_mode = db.get_pnotes(event.chat_id)
    if note["note"] == "Nil":
        caption = None
    else:
        caption = note["note"]
        if "{admin}" in caption:
            caption = caption.replace("{admin}", "")
            if event.is_group:
                if not await is_admin(event.chat_id, event.sender_id):
                    return
        elif "{private}" in caption:
            caption = caption.replace("{private}", "")
            p_mode = True
        elif "{noprivate}" in caption:
            caption = caption.replace("{noprivate}", "")
            p_mode = False
    if p_mode == False:
        file = id_tofile(note["id"], note["hash"], note["ref"], note["mtype"])
        if caption:
            caption, buttons = button_parser(caption)
        else:
            buttons = None
        if caption == "\n":
            caption = ""
        if caption:
                caption = await format_fill(event, caption)
        await event.respond(
            caption,
            file=file,
            buttons=buttons,
            parse_mode="md",
            reply_to=event.reply_to_msg_id or event.id,
        )
    else:
        await event.respond(
            "Tap here to view '{name}' in your private chat.",
            buttons=Button.url(
                "Click me",
                data=f"t.me/MissNeko_bot?start=notes_{event.chat_id}|{name}",
            ),
            reply_to=event.reply_to_msg_id or event.id,
        )


@Cbot(pattern="^/get ?(.*)")
async def get(event):
    name = event.pattern_match.group(1)
    if not name:
        return await event.reply("Not enough arguments!")
    note = db.get_note(event.chat_id, name)
    if not note:
        return await event.reply("No note found!")
    p_mode = db.get_pnotes(event.chat_id)
    if note["note"] == "Nil":
        caption = None
    else:
        caption = note["note"]
        if "{admin}" in caption:
            caption = caption.replace("{admin}", "")
            if event.is_group:
                if not await is_admin(event.chat_id, event.sender_id):
                    return
        elif "{private}" in caption:
            caption = caption.replace("{private}", "")
            p_mode = True
        elif "{noprivate}" in caption:
            caption = caption.replace("{noprivate}", "")
            p_mode = False
    if p_mode == False:
        file = id_tofile(note["id"], note["hash"], note["ref"], note["mtype"])
        if caption:
            caption, buttons = button_parser(caption)
            caption = await format_fill(event, caption)
        else:
            buttons = None
        await event.respond(
            caption,
            file=file,
            buttons=buttons,
            parse_mode="md",
            reply_to=event.reply_to_msg_id or event.id,
        )
    else:
        await event.respond(
            "Tap here to view '{name}' in your private chat.",
            buttons=Button.inline(
                "Click me",
                data=f"t.me/MissNeko_bot?start=notes_{event.chat_id}|{name}",
            ),
            reply_to=event.reply_to_msg_id or event.id,
        )


@Cbot(pattern="^/clear ?(.*)")
async def clear(event):
    if (
        event.text.startswith("+clearall")
        or event.text.startswith("/clearall")
        or event.text.startswith("?clearall")
        or event.text.startswith("!clearall")
    ):
        return
    if not event.from_id:
        return  # for now
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    try:
        args = event.text.split(None, 1)[1]
    except IndexError:
        args = None
    if not args:
        return await event.reply("Not enough arguments!")
    noted = db.get_note(event.chat_id, args)
    if noted:
        await event.reply("Note '{}' deleted!".format(args))
        return db.delete_note(event.chat_id, args)
    await event.reply("You haven't saved any notes with this name yet!")


@Cbot(pattern="^/(saved|Saved|Notes|notes)")
async def alln(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    p_mode = db.get_pnotes(event.chat_id)
    if p_mode:
        await event.respond(
            "Tap here to view all notes in this chat.",
            buttons=Button.url(
                "Click Me!",
                f"t.me/MissJessica_bot?start=allnotes_{event.chat_id}",
            ),
            reply_to=event.reply_to_msg_id or event.id,
        )
    else:
        notes = db.get_all_notes(event.chat_id)
        if not notes:
            return await event.reply(f"No notes in {event.chat.title}!")
        txt = f"List of notes in {event.chat.title}:"
        for a_note in notes:
            txt += f"\n- `#{a_note}`"
        txt += "\nYou can retrieve these notes by using `/get notename`, or `#notename`"
        await event.respond(txt, reply_to=event.reply_to_msg_id or event.id)


@Cbot(pattern="^/clearall")
async def delallfilters(event):
    if event.is_group:
        if event.from_id:
            if not await is_owner(event, event.sender_id):
                return
    buttons = [
        [Button.inline("Delete all notes", data="clearall")],
        [Button.inline("Cancel", data="cancelclearall")],
    ]
    text = f"Are you sure you would like to clear **ALL** notes in {event.chat.title}? This action cannot be undone."
    await event.reply(text, buttons=buttons)


@Cinline(pattern="clearall")
async def allcb(event):
    if not await cb_is_owner(event, event.sender_id):
        return
    await event.edit("Deleted all chat notes.", buttons=None)
    db.delete_all_notes(event.chat_id)


@Cinline(pattern="cancelclearall")
async def stopallcb(event):
    if not await cb_is_owner(event, event.sender_id):
        return
    await event.edit("Clearing of all notes has been cancelled.", buttons=None)


@Cbot(pattern="^/start notes_(.*)")
async def start_notes(event):
    data = event.pattern_match.group(1)
    chat, name = data.split("|", 1)
    chat_id = int(chat.strip())
    name = name.strip()
    note = db.get_note(chat_id, name)
    file = id_tofile(note["id"], note["hash"], note["ref"], note["mtype"])
    caption = note["note"]
    if caption:
        caption, buttons = button_parser(caption)
    else:
        buttons = None
    await event.reply(caption, file=file, buttons=buttons)


@Cbot(pattern="^/start allnotes_(.*)")
async def rr(event):
    chat_id = int(event.pattern_match.group(1))
    all_notes = db.get_all_notes(event.chat_id)
    OUT_STR = "**Notes:**\n"
    for a_note in all_notes:
        luv = f"{chat_id}_{a_note}"
        OUT_STR += f"- [{a_note}](t.me/MissJessica_bot?start=notes_{luv})\n"
    OUT_STR += "You can retrieve these notes by tapping on the notename."
    await event.reply(OUT_STR, link_preview=False)
