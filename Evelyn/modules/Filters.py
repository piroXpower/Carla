from Evelyn.events import Cbot

from . import can_change_info, get_reply_msg_btns_text
import Evelyn.modules.sql.filters_sql as sql

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
    

