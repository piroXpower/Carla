import re

from telethon import Button, events

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
    name = event.text
    if (
        name.startswith(".")
        or name.startswith("/")
        or name.startswith("?")
        or name.startswith("!")
    ):
        return
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
                pmode = "markdown"
                if "{html}" in text:
                    text = text.replace("{html}", "")
                    pmode = "html"
                text = await format_fill(event, text)
                await event.reply(text, file=file, buttons=buttons, parse_mode=pmode)


@Cbot(pattern="^/filters$")
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
            await event.reply(text, parse_mode="html")


@Cbot(pattern="^/stop ?(.*)")
async def estop(event):
    if (
        event.text.startswith(".stopall")
        or event.text.startswith("/stopall")
        or event.text.startswith("?stopall")
        or event.text.startswith("!stopall")
    ):
        return
    if event.is_private:
        return
    filter_name = event.pattern_match.group(1)
    if not filter_name:
        await event.reply("Not enough arguments provided.")
    all_filters = sql.get_all_filters(event.chat_id)
    for snips in all_filters:
        if snips.keyword == filter_name:
            await event.reply("Filter `'{}'` has been stopped!".format(snips.keyword))
            return sql.remove_filter(event.chat_id, snips.keyword)
    await event.reply("You haven't saved any filters on this word yet!")


@Cbot(pattern="^/stopall")
async def delallfilters(event):
    if event.is_private:
        return
    if event.is_group:
        if not await is_owner(event, event.sender_id):
            return
    buttons = [
        [Button.inline("Delete all filters", data="stopall")],
        [Button.inline("Cancel", data="cancelstopall")],
    ]
    text = f"Are you sure you would like to stop **ALL** filters in {event.chat.title}? This action cannot be undone."
    await event.reply(text, buttons=buttons)
