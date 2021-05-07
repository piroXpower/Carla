from Carla import tbot
from telethon import events
from Carla.events import Cbot
s = None
@Cbot(pattern="^/suz")
async def _(event):
 global s
 k = await tbot.get_reply_message()
 s = k

@tbot.on(events.InlineQuery)
async def h(e: events.InlineQuery.Event):
        global s
        builder = e.builder
        await e.answer(results=[
            builder.document(s, type='sticker')
        ])
