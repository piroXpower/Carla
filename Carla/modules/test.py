from Carla import tbot
from telethon import events
from Carla.events import Cbot
s = []
@Cbot(pattern="^/suz")
async def _(event):
 global s
 k = await event.get_reply_message()
 s.append(k)

@tbot.on(events.InlineQuery)
async def h(e: events.InlineQuery.Event):
        global s
        builder = e.builder
        sup = []
        for i in s:
         sup.append(await e.builder.document(i, type='gif'))
        await e.answer(sup, gallery=True)
