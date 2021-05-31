from telethon import Button, events

import Evelyn.modules.sql.notes_sql as sql
from Evelyn import tbot
from Evelyn.events import Cbot

from . import button_parser, can_change_info, get_reply_msg_btns_text, is_admin


@Cbot(pattern="^/save ?(.*)")
async def save(event):
    if event.is_private:
        return
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
        final = event.text.split(None, 1)[0]
        final = final.split(None, 1)
        if not len(final) == 2:
          return await event.reply("you need to give the note some content!")
        name = final[0]
        reply = final[1]
        file = None
    await event.reply(f"Saved note `{name}`")
    sql.add_note(event.chat_id, name, reply, file)


@Cbot(pattern="^/privatenotes ?(.*)")
async def pnotes(event):
    if event.is_private:
        return
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
    if event.is_private:
        return
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
    name = event.pattern_match.group(1)
    note = sql.get_notes(event.chat_id, name)
    if not note:
        return
    if event.is_reply:
        event.reply_to_msg_id
    else:
        event.id
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
        await event.reply(text, buttons=buttons)
    else:
        reply_text, buttons = button_parser(reply)
        if note.file:
            file = note.file
        else:
            file = None
        await event.reply(reply_text, buttons=buttons, file=file)
