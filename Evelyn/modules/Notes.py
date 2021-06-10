from telethon import Button, events

import Evelyn.modules.sql.notes_sql as sql
from Evelyn import tbot
from Evelyn.events import Cbot

from . import (
    button_parser,
    can_change_info,
    cb_is_owner,
    format_fill,
    get_reply_msg_btns_text,
    is_admin,
    is_owner,
)


@Cbot(pattern="^/save ?(.*)")
async def save(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await anonymous_save(event)
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    if not event.pattern_match.group(1) and not event.is_reply:
        return await event.reply("You need to give the note a name!")
    elif event.is_reply:
        if not event.pattern_match.group(1):
            return await event.reply("You need to give the note a name!")
        name = event.pattern_match.group(1)
        msg = await event.get_reply_message()
        if msg.media and not msg.text:
            file = msg.file.id
            reply = ""
        elif msg.media and msg.text:
            file = msg.file.id
            reply = msg.text
        elif msg.text:
            file = None
            reply = msg.text
        if msg.reply_markup:
            buttons = get_reply_msg_btns_text(msg)
            reply = reply + " " + str(buttons)
    elif event.pattern_match.group(1):
        final = event.text.split(None, 1)[1]
        final_i = final.split(None, 1)
        if not len(final_i) == 2:
            return await event.reply("you need to give the note some content!")
        name = final_i[0]
        reply = final_i[1]
        file = None
    await event.reply(f"Saved note `{name}`")
    sql.add_note(event.chat_id, name, reply, file)


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
        mode = sql.get_mode(event.chat_id)
        if mode:
            text = "Your notes are currently being sent in private. Evelyn will send a small note with a button which redirects to a private chat."
        else:
            text = "Your notes are currently being sent in the group."
        await event.reply(text)
    elif arg in ["y", "yes", "on", "true"]:
        await event.reply(
            "Evelyn will now send a message to your chat with a button redirecting to PM, where the user will receive the note."
        )
        sql.set_mode(event.chat_id, True)
    elif arg in ["n", "no", "off", "false"]:
        await event.reply("Evelyn will now send notes straight to the group.")
        sql.set_mode(event.chat_id, False)
    else:
        await event.reply(
            f"failed to get boolean value from input: expected one of y/yes/on or n/no/off; got: {arg}"
        )


@Cbot(pattern="^/clear ?(.*)")
async def clear(event):
    if (
        event.text.startswith(".clearall")
        or event.text.startswith("/clearall")
        or event.text.startswith("?clearall")
        or event.text.startswith("!clearall")
    ):
        return
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return  # for now
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    args = event.pattern_match.group(1)
    if not args:
        return await event.reply("Not enough arguments!")
    notes = sql.get_all_notes(event.chat_id)
    for note in notes:
        if note.keyword == args:
            await event.reply("Note '{}' deleted!".format(args))
            return sql.remove_note(event.chat_id, args)
    await event.reply("You haven't saved any notes with this name yet!")


@tbot.on(events.NewMessage(pattern=r"\#(\S+)"))
async def nottrig(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    name = event.pattern_match.group(1)
    note = sql.get_notes(event.chat_id, name)
    if not note:
        return
    if event.is_reply:
        rep = event.reply_to_msg_id
    else:
        rep = event.id
    mode = sql.get_mode(event.chat_id)
    reply = note.reply
    if "{private}" in reply:
        reply = (reply).replace("{private}", "")
        mode = True
    if "{noprivate}" in reply:
        reply = (reply).replace("{noprivate}", "")
        mode = False
    if mode:
        if "{admin}" in reply:
            reply = (reply).replace("{admin}", "")
            if not await is_admin(event.chat_id, event.sender_id):
                return
        reply_text = "Tap here to view '{}' in your private chat.".format(name)
        buttons = Button.url(
            "Click Me", f"t.me/MissEvelyn_bot?start=notes_{event.chat_id}&{name}"
        )
        await tbot.send_message(
            event.chat_id,
            reply_text,
            buttons=buttons,
            reply_to=event.reply_to_msg_id or event.id,
        )
    else:
        if "{admin}" in reply:
            reply = (reply).replace("{admin}", "")
            if not await is_admin(event.chat_id, event.sender_id):
                return
        reply_text, buttons = button_parser(reply)
        if note.file:
            file = note.file
        else:
            file = None
        reply_final = await format_fill(event, reply_text)
        await tbot.send_message(
            event.chat_id,
            reply_final,
            buttons=buttons,
            file=file,
            reply_to=rep,
            parse_mode="html",
        )


@Cbot(pattern="^/get ?(.*)")
async def nottrig(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    name = event.pattern_match.group(1)
    if not name:
        return await event.reply("Not enough arguments!")
    note = sql.get_notes(event.chat_id, name)
    if not note:
        return await event.reply("Note not found.")
    if event.is_reply:
        rep = event.reply_to_msg_id
    else:
        rep = event.id
    mode = sql.get_mode(event.chat_id)
    reply = note.reply
    if "{private}" in reply:
        reply = (reply).replace("{private}", "")
        mode = True
    if "{noprivate}" in reply:
        reply = (reply).replace("{noprivate}", "")
        mode = False
    if mode:
        if "{admin}" in reply:
            reply = (reply).replace("{admin}", "")
            if not await is_admin(event.chat_id, event.sender_id):
                return
        text = "Tap here to view '{}' in your private chat.".format(name)
        buttons = Button.url(
            "Click Me", f"t.me/MissEvelyn_bot?start=notes_{event.chat_id}&{name}"
        )
        await tbot.send_message(
            event.chat_id,
            text,
            buttons=buttons,
            reply_to=event.reply_to_msg_id or event.id,
        )
    else:
        if "{admin}" in reply:
            reply = (reply).replace("{admin}", "")
            if not await is_admin(event.chat_id, event.sender_id):
                return
        reply_text, buttons = button_parser(reply)
        if note.file:
            file = note.file
        else:
            file = None
        reply_final = await format_fill(event, reply_text)
        await tbot.send_message(
            event.chat_id,
            reply_final,
            buttons=buttons,
            file=file,
            reply_to=rep,
            parse_mode="html",
        )


@Cbot(pattern="^/clearall")
async def delallfilters(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
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


@tbot.on(events.CallbackQuery(pattern="clearall"))
async def stopallcb(event):
    if not await cb_is_owner(event, event.sender_id):
        return
    await event.edit("Deleted all chat notes.", buttons=None)
    sql.remove_all_notes(event.chat_id)


@tbot.on(events.CallbackQuery(pattern="cancelclearall"))
async def stopallcb(event):
    if not await cb_is_owner(event, event.sender_id):
        return
    await event.edit("Clearing of all notes has been cancelled.", buttons=None)


@Cbot(pattern="^/(saved|Saved|Notes|notes)")
async def alln(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    mode = sql.get_mode(event.chat_id)
    if mode:
        buttons = Button.inline(
            "Click Me!", f"t.me/MissEvelyn_bot?start=notes_{event.chat_id}&all"
        )
        await event.respond(
            "Tap here to view all notes in this chat.",
            buttons=buttons,
            reply_to=event.reply_to_msg_id or event.id,
        )
    else:
        notes = sql.get_all_notes(event.chat_id)
        if not notes:
            return await event.reply(f"No notes in {event.chat.title}!")
        txt = f"List of notes in {event.chat.title}:"
        for note in notes:
            txt += f"\n- `{note.keyword}`"
        txt += "\nYou can retrieve these notes by using `/get notename`, or `#notename`"
        await event.respond(txt, reply_to=event.reply_to_msg_id or event.id)


@Cbot(pattern="^/start notes_(.*)&(.*)")
async def start_notes(event):
    chat_id = int(event.pattern_match.group(1))
    name = event.pattern_match.group(1)
    notes = sql.get_all_notes(event.chat_id)
    if name == "all":
        txt = f"List of notes in `{chat_id}`:"
        for note in notes:
            txt += f"- [{note.keyword}](t.me/MissCarla_bot?start=notes_{chat_id}&{note.keyword})"
        txt += "You can retrieve these notes by tapping on the notename."
    else:
        note = sql.get_notes(event.chat_id, name)
        txt += "**{note.keyword}**"
        txt += "\n" + note.reply
    await event.reply(txt)
