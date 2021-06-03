from telethon import events

from Evelyn.events import Cquery


@Cquery(pattern="cq ?(.*)")
async def cq(event: events.InlineQuery.Event):
    try:
        builder = event.builder
        query = event.pattern_match.group(1)
        if query == None or len(query) > 4096:
            title = "🔥 Write a whisper message"
            content = "**Send whisper messages through inline mode**\n\nUsage: `@ezWhisperBot [@username] text`"
            des = "Usage: @ezWhisperBot [@username] text"
            icon_url = "https://www.freeiconspng.com/uploads/whisper-icon-0.png"
            result = builder.article(
                title=title,
                description=content,
                text=des,
                thumb=icon_url,
            )
            await event.answer([result])
    except Exception as e:
        print(e)
