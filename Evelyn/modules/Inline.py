from telethon import Button

from Evelyn.events import Cquery


@Cquery(pattern="cq ?(.*)")
async def cq(event):
    builder = event.builder
    query = event.pattern_match.group(1)
    if query == "" or len(query) > 4096:
        title = "🔥 Write a whisper message"
        content = (
            "**Send whisper messages through inline mode**\n\n"
            "Usage: `@ezWhisperBot [@username] text`"
        )
        description = "Usage: @ezWhisperBot [@username] text"
        icon_url = "https://www.freeiconspng.com/uploads/whisper-icon-0.png"
        result = builder.article(
            title=title,
            description=content,
            text=description,
            thumb=icon_url,
            buttons=[
                [Button.switch_inline("Learn more", query="yt ", same_peer=True)],
            ],
        )
        await event.answer([result])
