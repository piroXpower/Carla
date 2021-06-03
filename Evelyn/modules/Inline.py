from telethon import Button, events

from Evelyn.events import Cquery


@Cquery(pattern="cq ?(.*)")
async def cq(event: events.InlineQuery.Event):
    builder = event.builder
    query = event.pattern_match.group(1)
    if query == "" or len(query) > 4096:
        content = "**Send whisper messages through inline mode**\n\nUsage: `@MissEvelyn_Bot [@username] text`"
        des = "Usage: @MissEvelyn_Bot [@username] text"
        icon_url = "https://www.freeiconspng.com/uploads/whisper-icon-0.png"
        resultm = builder.article(
            title="🔥 Write a whisper message",
            description=des,
            text=content,
            buttons=[
                [Button.switch_inline("Make New", query="cq ", same_peer=True)],
            ],
        )
        await event.answer([resultm])
    elif not query.startswith("@"):
        content = "👀 The first one who open the whisper can read it"
        des = f"🤫 {query}"
        buttons = [
            [Button.inline("👀 show message", data="show_whisper")],
        ]
        resultm = builder.article(
            title="🔥 Write a whisper message",
            description=des,
            text=content,
            buttons=buttons,
        )
        await event.answer([resultm])
# soon

@Cquery(pattern="pypi ?(.*)")
async def pypi(event):
 builder = event.builder
 query = event.pattern_match.group(1)
 title = "PYPi search"
 if not query:
   des = "Please input the name of a pypi library to gather it's info."
   result = builder.article(title=title, description=des, text=des, buttons=[
                [Button.switch_inline("Search again", query="pypi ", same_peer=True)],
            ],)
   await event.answer([result])


        
