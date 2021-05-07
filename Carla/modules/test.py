from Carla import tbot

sticker = 'CAADBQAD0gEAAjAnSjiO_2DuZwa5tgI'

@tbot.on(events.InlineQuery)
async def h(e: events.InlineQuery.Event):
        builder = e.builder
        await e.answer(results=[
            builder.document(sticker, type='sticker')
        ])
