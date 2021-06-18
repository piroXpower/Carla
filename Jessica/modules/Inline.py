from requests import get
from telethon import Button, events
from telethon.tl.types import InputWebDocument

from Jessica import tbot
from Jessica.events import Cquery


@tbot.on(events.InlineQuery(pattern=None))
async def nan(event):
    builder = event.builder
    text = event.text
    text = text.replace("@MissCarla_Bot", "")
    if not text == "":
        return
    icon = InputWebDocument(
        url="https://telegra.ph/file/e3d2fb68aeb79548f1be9.jpg",
        size=1142,
        mime_type="image/jpeg",
        attributes=[],
    )
    results = []
    title_1 = "Jessica Bot"
    title_2 = "Inline Help"
    des_2 = "Open Inline Help Menu"
    des_1 = "Bot Info and status"
    content_1 = gen_status()
    content_2 = "Hi for now"
    result_1 = builder.article(
        title=title_1,
        description=des_1,
        text=content_1,
        thumb=icon,
    )
    result_2 = builder.article(
        title=title_2,
        description=des_2,
        text=content_2,
        thumb=icon,
    )
    results.append(result_1)
    results.append(result_2)
    await event.answer(results)


def gen_status():
    txt = "**Jessica Bot Info**:"
    txt += "\nServer: Heroku"
    txt += "\nDatabase: MongoDB"
    txt += "\nTelethon: 1.21.1"
    txt += "\nPython: 3.9.5"
    return txt


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
        content = "**Send whisper messages through inline mode**\n\nUsage: `@MissJessica_Bot [@username] text`"
        des = "Usage: @MissJessica_Bot [@username] text"
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