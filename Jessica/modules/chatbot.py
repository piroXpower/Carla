from telethon import events

import Jessica.modules.sql.chatbot_sql as sql
from Jessica import BOT_ID, CMD_HELP, tbot, ubot
from Jessica.events import Cbot

from . import can_change_info


@Cbot(pattern="^/chatbot ?(.*)")
async def cb(event):
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    args = event.pattern_match.group(1)
    if not args:
        mode = sql.chatbot_mode(event.chat_id)
        if mode:
            await event.reply("AI chatbot is currently **enabled** for this chat.")
        else:
            await event.reply("AI chatbot is currently **disabled** for this chat.")
    elif args in ["on", "y", "yes"]:
        await event.reply("**Enabled** AI chatbot for this chat.")
        sql.set_chatbot_mode(event.chat_id, True)
    elif args in ["off", "n", "no"]:
        await event.reply("**Disabled** AI chatbotfor this chat.")
        sql.set_chatbot_mode(event.chat_id, False)
    else:
        await event.reply("Your input was not recognised as one of: yes/no/y/n/on/off")


@tbot.on(events.NewMessage())
async def cb(e):
    if not sql.chatbot_mode(e.chat_id):
        return
    if e.media:
        return
    if e.reply_to:
        r_e = await e.get_reply_message()
        if r_e.sender_id == int(BOT_ID):
            pass
        else:
            return
    elif "neko" in (e.text).lower():
        pass
    else:
        return
    q = e.text
    for x in [".", "!", "/", "?"]:
        if q.startswith(x):
            return
    if "neko" in q.lower():
        q = (q.lower()).replace("neko", "kuki")
    async with tbot.action(e.chat_id, "typing"):
        async with ubot.conversation("@KukiAI_bot") as chat:
            await chat.send_message(str(q))
            res = await chat.get_response()
            if res.text:
                response = res.text
                if "Bad Request" in response:
                    return
                if "weather" in q.lower():
                    try:
                        await ubot.send_read_acknowledge(chat.chat_id)
                        res_2 = await chat.get_response()
                        if "Bad Request" in res_2.text:
                            return
                        await ubot.send_read_acknowledge(chat.chat_id)
                        res_3 = await chat.get_response()
                        response = res_3.text
                        if "Bad Request" in res_3.text:
                            return
                    except:
                        pass
            elif res.media:
                if "weather" in q.lower():
                    try:
                        await ubot.send_read_acknowledge(chat.chat_id)
                        res_2 = await chat.get_response()
                        if "Bad Request" in res_2.text:
                            return
                        await ubot.send_read_acknowledge(chat.chat_id)
                        res_3 = await chat.get_response()
                        if "Bad Request" in res_3.text:
                            return
                        response = res_3.text
                    except:
                        pass
                else:
                    await ubot.send_read_acknowledge(chat.chat_id)
                    res_2 = await chat.get_response()
                    if res_2.text:
                        response = res_2.text
                    else:
                        return
            if not response:
                return
            for x in ["Kuki", "kuki.", "Kuki.", "kuki"]:
                response = response.replace(x, "Neko")
            if "Fams" in response:
                response = response.replace("Fams", str(e.sender.first_name))
            await e.reply(response)


__name__ = "chatbot"
__help__ = """
AI CHAT-BOT

__Admin__
- /chatbot <on/off>: enables or disables the ai chatbot

The AI replies to anyone who tags the bot or mentions "Neko" in their text.
"""
CMD_HELP.update({__name__: [__name__, __help__]})
