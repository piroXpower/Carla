from Carla import tbot
from telethon import events
from Carla.events import Cbot
s = []
@Cbot(pattern="^/suz")
async def _(event):
 global s
 k = await event.get_reply_message()
 m = await tbot.download_media(event.chat_id, k, './')
 s.append(m)
 await event.respond('Done')

@tbot.on(events.InlineQuery)
async def h(e: events.InlineQuery.Event):
        global s
        builder = e.builder
        await e.answer(results=[
            builder.document(s, text='suck my dick', type='photo')
        ], gallery=True)
