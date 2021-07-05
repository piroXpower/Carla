from PIL import Image, ImageDraw, ImageFont
from requests import get
from telethon import Button, events
from telethon.tl.types import InputWebDocument
from youtubesearchpython import SearchVideos

from Jessica import tbot
from Jessica.events import Cinline, Cquery

whisper_db = {}


@tbot.on(events.InlineQuery(pattern=None))
async def nan(event):
    builder = event.builder
    text = event.text
    text = text.replace("@MissNeko_Bot", "")
    if not text == "":
        return
    icon = InputWebDocument(
        url="https://telegra.ph/file/e3d2fb68aeb79548f1be9.jpg",
        size=1142,
        mime_type="image/jpeg",
        attributes=[],
    )
    results = []
    title_1 = "NekoChan"
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
    txt = "**NekoChan Info**:"
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
        des = "Usage: @MissNeko_Bot [@username] text"
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
        whisper_db[event.id] = des
        cb_data = str(event.id) + "|" + "Nil"
        buttons = [
            [Button.inline("👀 show message", data="show_whisper_{}".format(cb_data))],
        ]
        resultm = builder.article(
            title="🔥 Write a whisper message",
            description=des,
            text=content,
            thumb=icon,
            buttons=buttons,
        )
        await event.answer([resultm])


@Cinline(pattern=r"show_whisper(\_(.*))")
async def whisper_message(event):
    input = (((event.pattern_match.group(1)).decode()).split("_", 1)[1]).split("|")
    rec_id = input[0]
    reply_to = input[1]
    print(rec_id)
    if not reply_to == "Nil":
        if not event.sender_id == int(reply_to):
            return await event.answer("This was not send for you!", alert=True)
    try:
        w_message = whisper_db[int(rec_id)]
    except KeyError:
        return await event.edit("Whisper Message not found.", buttons=None)
    await event.answer(str(w_message), alert=True)
    await event.edit(buttons=None)


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


@Cquery(pattern="yt ?(.*)")
async def yt_q(event):
    builder = event.builder
    query = event.pattern_match.group(1)
    results = []
    search = SearchVideos(query, offset=1, mode="dict", max_results=5)
    if not search:
        result = builder.article(
            title="No Results.",
            description="Try Again With correct Spelling",
            text="**No Matching Found**",
            buttons=[
                [Button.switch_inline("Search Again", query="yt ", same_peer=True)],
            ],
        )
        results.append(result)
    else:
        for x in (search.result())["search_result"]:
            link = x["link"]
            title = x["title"]
            duration = x["duration"]
            channel = x["channel"]
            views = x["views"]
            icon = InputWebDocument(
                url="https://img.youtube.com/vi/{}/hqdefault.jpg".format(x["id"]),
                size=142,
                mime_type="image/jpeg",
                attributes=[],
            )
            results.append(
                await event.builder.article(
                    title=title,
                    description=channel,
                    text=f"Title: {title}\nLink: {link}\nChannel: {channel}\nDuration: <code>{duration}</code>\nViews: {views}",
                    thumb=icon,
                    parse_mode="html",
                    link_preview=True,
                    buttons=Button.switch_inline(
                        "Search Again", query="yt ", same_peer=True
                    ),
                )
            )
    await event.answer(results)


@Cquery(pattern="doge ?(.*)")
async def doge(event):
    builder = event.builder
    N = event.pattern_match.group(1)
    if not N:
        return
    image = Image.open("Jessica/modules/sql/IMG_20210705_134908_649.jpg")
    font = ImageFont.truetype(
        "Jessica/modules/sql/FontsFree-Net-Ambiguity-radical.ttf", 70
    )
    draw = ImageDraw.Draw(image)
    image_widthz, image_heightz = image.size
    w, h = draw.textsize(str(N), font=font)
    h += int(h * 0.21)
    draw.text(
        ((image_widthz - w) / 2, (image_heightz - h) / 2),
        str(N),
        font=font,
        fill="black",
    )
    x = (image_widthz - w) / 2
    y = (image_heightz - h) / 2
    draw.text(
        (x, y), str(N), font=font, fill="black", stroke_width=1, stroke_fill="black"
    )
    image.save("mk.jpg")
    result = builder.photo("mk.jpg")
    await event.answer([result], gallery=True)
