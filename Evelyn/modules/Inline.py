from requests import get
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
        des = "You haven't given anything to search."
        result = builder.article(
            title=title,
            description=des,
            text=des,
            buttons=[
                [Button.switch_inline("Search again", query="pypi ", same_peer=True)],
            ],
        )
        await event.answer([result])
    else:
        url = f"https://pypi.org/pypi/{query}/json"
        response = get(url)
        if not response:
            des = "Invalid pypi package provided!"
            con = des
            buttons = (
                [Button.switch_inline("Search again", query="pypi ", same_peer=True)],
            )

        else:
            result = response.json()
            name = (result["info"]["name"]).capitalize()
            author = result["info"]["author"]
            version = result["info"]["version"]
            summary = result["info"]["summary"]
            release_url = result["info"]["release_url"]
            requires_dist = result["info"]["requires_dist"]
            py = f"<b><h1>{name}</h1></b>"
            py += f"\n\n<b>Author:</b> {author}"
            py += f"\n<b>Latest Version:</b> <code>{version}</code>"
            if summary:
                py += f"\n\n<b>Summary:</b> <i>{summary}</i>"
            if release_url:
                py += f"\n\n<b>URL:</b> <code>{release_url}</code>"
            if requires_dist:
                py += f"\n<b>Dependencies:</b>\n{requires_dist}"
            des = py
            con = name + "\n" + "Author: " + author
            buttons = Button.switch_inline(
                "Search again", query="pypi ", same_peer=True
            ), Button.url(name, f"https://pypi.org/pypi/{name}")
        result = builder.article(
            title=title, description=des, text=con, buttons=buttons
        )
        await event.answer([result])
