from Evelyn.events import Cquery


@Cquery(pattern="cq")
async def cq(event):
    await event.answer("Hello")
