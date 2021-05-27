import re

from telethon import events

import Evelyn.modules.sql.filters_sql as sql
from Evelyn.events import Cbot

from . import button_parser, can_change_info, format_fill, get_reply_msg_btns_text


@Cbot(pattern="^/filter ?(.*)")
async def filter(event):
    if (
        event.text.startswith("!filters")
        or event.text.startswith("/filters")
        or event.text.startswith("?filters")
        or event.text.startswith(".filters")
    ):
        return
    if event.is_private:
        return
    if event.is_group:
        if event.from_id:
            if not await can_change_info(event, event.sender_id):
                return
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        return await event.reply("You need to give the filter a name!")
    elif event.reply_to_msg_id:
        if not event.pattern_match.group(1):
            return await event.reply("You need to give the filter a name!")
        else:
            msg = await event.get_reply_message()
            name = event.pattern_match.group(1)
            if msg.media and not msg.text:
                file = msg.file.id
                reply = ""
            elif msg.media and msg.text:
                file = msg.file.id
                reply = msg.text
            else:
                file = ""
                reply = msg.text
            buttons = ""
            if msg.reply_markup:
                buttons = get_reply_msg_btns_text(msg)
            reply = reply + " " + str(buttons)
    elif not event.reply_to_msg_id and event.pattern_match.group(1):
        total = event.text.split(None, 1)[1]
        total = total.split(" ", 1)
        if len(total) == 1:
            return await event.reply("You need to give the filter some content!")
        name = total[0]
        reply = total[1]
        file = ""
    await event.reply(f"Saved filter '{name}'.")
    sql.add_filter(event.chat_id, name, reply, file)


@tbot.on(events.NewMessage())
async def newfiltertrugger(event):
    if event.is_private:
        return
    if (
        event.text.startswith(".")
        or event.text.startswith("/")
        or event.text.startswith("?")
        or event.text.startswith("!")
    ):
        return
    name = event.text
    snips = sql.get_all_filters(event.chat_id)
    if snips:
        for snip in snips:
            pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
            if re.search(pattern, name, flags=re.IGNORECASE):
                file = snip.file
                if file == "":
                    file = None
                reply = snip.reply
                buttons = None
                text = ""
                if not reply == "":
                    text, buttons = button_parser(reply)
                text = await format_fill(event, text)
                await event.reply(text, file=file, buttons=buttons, parse_mode="HTML")

@Cbot(pattern"^/filters$")
async def filter(event):
 if event.is_private:
     return
 snips = sql.get_all_filters(event.chat_id)
 if snips:
   if len(snips) == 0:
     await event.reply(f"No filters in {event.chat.title}!")
   else:
     text = "<b>Filters in {}:</b>".format(event.chat.title)
     for snip in snips:
        text += "\n- <code>{}</code>".format(snip.keyword)
     await event.reply(text)
