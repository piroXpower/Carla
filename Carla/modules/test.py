from Carla import tbot
from telethon import events
from Carla.events import Cbot
s = []
@Cbot(pattern="^/suz")
async def _(event):
 global s
 k = await tbot.get_reply_message()
 s.append(k)

@tbot.on(events.InlineQuery)
async def h(e: events.InlineQuery.Event):
        global s
        builder = e.builder
        for i in s
         await e.answer(results=[
            builder.document(i, type='sticker')
        ])
