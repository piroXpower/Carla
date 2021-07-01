import asyncio

from telethon import events

import Jessica.modules.sql.chatbot_sql as sql
from Jessica import BOT_ID, tbot, ubot
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
    else:
        return
    q = e.text
    for x in [".", "!", "/", "?"]:
        if q.startswith(x):
            return
    async with tbot.action(e.chat_id, "typing"):
        async with ubot.conversation("@KukiAI_bot") as chat:
            await chat.send_message(str(q))
            await asyncio.sleep(1)
            res = await chat.get_response()
            if res.text:
                response = res.text
            else:
                return
            for x in ["Kuki", "kuki.", "Kuki."]:
                response = response.replace(x, "Neko")
            await e.reply(response)


@ubot.on(events.NewMessage(from_users=(["@KukiAI_bot"])))
async def e(e):
    if e.media:
        await e.delete()
