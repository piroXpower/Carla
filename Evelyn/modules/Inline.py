from telethon import Button, events

from Evelyn.events import Cquery


@Cquery(pattern="cq ?(.*)")
async def cq(event: events.InlineQuery.Event):
    builder = event.builder
    query = event.pattern_match.group(1)
    if query == "" or len(query) > 4096:
        content = "**Send whisper messages through inline mode**\n\nUsage: `@ezWhisperBot [@username] text`"
        des = "Usage: @ezWhisperBot [@username] text"
        icon_url = "https://www.freeiconspng.com/uploads/whisper-icon-0.png"
        resultm = builder.article(
            title="🔥 Write a whisper message",
            description=des,
            text=content,
            buttons=[
                [Button.switch_inline("Search Again", query="cq ", same_peer=True)],
            ],
        )
        await event.answer([resultm])
