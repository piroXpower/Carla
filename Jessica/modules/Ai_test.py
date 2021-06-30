from telethon import events

from Jessica import ubot
from Jessica.events import Cbot


@Cbot(pattern="^/c ?(.*)")
async def cb(e):
    q = e.pattern_match.group(1)
    if not q:
        return
    async with ubot.conversation("@KukiAI_bot") as chat:
        await chat.send_message(str(q))
        res = await chat.get_response()
        if res.media:

            @ubot.on(events.NewMessage(from_users=(["@KukiAI_bot"])))
            async def _(ev):
                await e.reply(ev.text)

        elif res.text:
            await e.reply(res.text)
