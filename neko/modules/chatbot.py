from telethon import.utils

from .. import BOT_ID, CMD_HELP, tbot, ubot
from ..utils import Cbot
from . import can_change_info
from .mongodb.chatbot_db import is_chat, set_chatbot


@Cbot(pattern="^/chatbot ?(.*)")
async def chatbot_s(e):
    if e.is_group:
        if not await can_change_info(e, e.sender_id):
            return
    args = e.pattern_match.group(1)
    if not args:
        mode = is_chat(e.chat_id)
        if mode:
            await e.reply("AI chatbot is currently **enabled** for this chat.")
        else:
            await e.reply("AI chatbot is currently **disabled** for this chat.")
    elif args in ["on", "y", "yes"]:
        await e.reply("**Enabled** AI chatbot for this chat.")
        set_chatbot(e.chat_id, True)
    elif args in ["off", "n", "no"]:
        await e.reply("**Disabled** AI chatbot for this chat.")
        set_chatbot(e.chat_id, False)
    else:
        await e.reply("Your input was not recognised as one of: yes/no/y/n/on/off")


@tbot.on.utils.NewMessage())
async def cb(e):
    if not is_chat(e.chat_id):
        return
    if e.media:
        return
    if e.reply_to:
        r_e = await e.get_reply_message()
        if r_e and r_e.sender_id:
            pass
        else:
            return
        if r_e.sender_id == int(BOT_ID):
            pass
        else:
            return
    elif "neko" in (e.text).lower():
        pass
    else:
        return
    q = e.text
    for x in [".", "!", "/", "?", "+"]:
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
Here is the help for **Chatbot** module:

**Admin Commands**
- /chatbot `<on/off>`: Enables or Disables the AI chatbot

The **AI** replies to anyone who tags the bot or mentions "Neko" in their text.
"""
CMD_HELP.update({__name__: [__name__, __help__]})
