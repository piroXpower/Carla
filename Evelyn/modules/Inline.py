from telethon import events, Button

from Evelyn.events import Cquery


@Cquery(pattern="cq ?(.*)")
async def cq(event: events.InlineQuery.Event):
        builder = event.builder
        query = event.pattern_match.group(1)
        if query == '' or len(query) > 4096:
            title = "🔥 Write a whisper message"
            content = "**Send whisper messages through inline mode**\n\nUsage: `@ezWhisperBot [@username] text`"
            des = "Usage: @ezWhisperBot [@username] text"
            icon_url = "https://www.freeiconspng.com/uploads/whisper-icon-0.png"
            resultm = builder.article(
                title="No Results.",
                description="Try Again With correct Spelling",
                text="**No Matching Found**",
                buttons=[
                    [Button.switch_inline("Search Again", query="yt ", same_peer=True)],
                ],
            )
            await event.answer([resultm])
