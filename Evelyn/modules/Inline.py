from requests import get
from telethon import Button, events
from telethon.tl.types import InputWebDocument

from Evelyn.events import Cquery


@tbot.on(events.InlineQuery(pattern=None))
async def nan(event):
    text = event.text
    text = text.replace("@MissCarla_Bot", "")
    if not text == "":
        return
    print("inline aa")


@Cquery(pattern="cq ?(.*)")
async def cq(event: events.InlineQuery.Event):
    builder = event.builder
    query = event.pattern_match.group(1)
    icon = InputWebDocument(
        url="https://www.freeiconspng.com/uploads/whisper-icon-0.png",
        size=142,
        mime_type="image/jpeg",
        attributes=[],
    )
    if query == "" or len(query) > 4096:
        content = "**Send whisper messages through inline mode**\n\nUsage: `@MissEvelyn_Bot [@username] text`"
        des = "Usage: @MissEvelyn_Bot [@username] text"
        icon_url = "https://www.freeiconspng.com/uploads/whisper-icon-0.png"
        resultm = builder.article(
            title="🔥 Write a whisper message",
            description=des,
            text=content,
            thumb=icon,
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
            thumb=icon,
            buttons=buttons,
        )
        await event.answer([resultm])


# soon


@Cquery(pattern="pypi ?(.*)")
async def pypi(event):
    builder = event.builder
    query = event.pattern_match.group(1)
    title = "PYPi search"
    icon = InputWebDocument(
        url="https://pypi.org/static/images/twitter.90915068.jpg",
        size=142,
        mime_type="image/jpeg",
        attributes=[],
    )
    if not query:
        des = "You haven't given anything to search."
        result = builder.article(
            title=title,
            description=des,
            text=des,
            thumb=icon,
            buttons=[
                [Button.switch_inline("Search again", query="pypi ", same_peer=True)],
            ],
        )
        await event.answer([result])
    else:
        url = f"https://pypi.org/pypi/{query}/json"
        response = get(url)
        if not response:
            des = f"No results found for {query}!"
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
            py = f"**{name}**"
            py += f"\n\n**Author:** {author}"
            py += f"\n**Latest Version:** `{version}`"
            if summary:
                py += f"\n\n**Summary:** __{summary}__"
            if release_url:
                py += f"\n\n**URL:** `{release_url}`"
            if requires_dist:
                py += f"\n**Dependencies:**\n{requires_dist}"
            des = py
            con = name + "\n" + "Author: " + author
            buttons = Button.switch_inline(
                "Search again", query="pypi ", same_peer=True
            ), Button.url(name, f"https://pypi.org/project/{name}")
        result = builder.article(
            title=title,
            description=con,
            text=des,
            buttons=buttons,
            thumb=icon,
        )
        await event.answer([result])
