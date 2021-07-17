from bs4 import BeautifulSoup
from GoogleNews import GoogleNews
from PIL import Image, ImageDraw, ImageFont
from requests import get
from telethon import Button, events
from telethon.tl.types import InputWebDocument
from tpblite import TPB
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
    txt += "\nTelethon: 1.22"
    txt += "\nPython: 3.9.7"
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
    icon = InputWebDocument(
        url="https://pypi.org/static/images/twitter.90915068.jpg",
        size=142,
        mime_type="image/jpeg",
        attributes=[],
    )
    if not query:
        x = get("https://pypi.org/")
        soup = BeautifulSoup(x.text, "html.parser")
        q = soup.findAll("ul", attrs={"aria-labelledby": "pypi-trending-packages"})
        if not q:
            return
        pnames = q[0].find_all("span", attrs={"class": "package-snippet__name"})
        versions = q[0].find_all("span", attrs={"class": "package-snippet__version"})
        descriptions = q[0].find_all(
            "p", attrs={"class": "package-snippet__description"}
        )
        x = -1
        result = []
        for _x in pnames:
            x += 1
            des = f"Package: **{(_x.text).capitalize()}**\n\n**Latest Version:** `{versions[x].text}`"
            if descriptions[x].text:
                des += f"\n\n**Description:** __{descriptions[x].text}__"
            result.append(
                await builder.article(
                    title=str(_x.text),
                    description=str(versions[x].text) + "\n" + descriptions[x].text,
                    text=str(des),
                    buttons=[
                        Button.switch_inline(
                            "Search again", query="pypi ", same_peer=True
                        ),
                        Button.url(
                            _x.text,
                            f"https://pypi.org/project/{_x.text}/{versions[x].text}/",
                        ),
                    ],
                    thumb=icon,
                )
            )
        await event.answer(result)
    else:
        url = f"https://pypi.org/search/?q={query}"
        response = get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        q = soup.find("ul", attrs={"aria-label": "Search results"})
        if not q:
            return
        pnames = q.findAll("span", attrs={"class": "package-snippet__name"})
        versions = q.findAll("span", attrs={"class": "package-snippet__version"})
        descriptions = q.findAll("p", attrs={"class": "package-snippet__description"})
        times = q.find_all("span", attrs={"class": "package-snippet__released"})
        x = -1
        f = []
        for _x in pnames:
            x += 1
            des = f"Package: **{(_x.text).capitalize()}**\n\n**Latest Version:** `{versions[x].text}`\n**Last Updated:** `{times[x].time.text}`"
            if descriptions[x].text:
                des += f"\n**Description:** __{descriptions[x].text}__"
            f.append(
                await builder.article(
                    title=str(_x.text),
                    description=str(versions[x].text) + "\n" + descriptions[x].text,
                    text=str(des),
                    buttons=[
                        Button.switch_inline(
                            "Search again", query="pypi ", same_peer=True
                        ),
                        Button.url(
                            _x.text,
                            f"https://pypi.org/project/{_x.text}/{versions[x].text}/",
                        ),
                    ],
                    thumb=icon,
                )
            )
        await event.answer(f)


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


@Cquery(pattern="imdb ?(.*)")
async def imdb_q(e):
    query = e.pattern_match.group(1)
    if not query:
        return
    url = f"https://www.imdb.com/find?q={query}&ref_=nv_sr_sm"
    r = get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find_all("div", attrs={"class": "findSection"})
    results = div[0].findAll("td", attrs={"class": "result_text"})
    pop_result = []
    thumb = InputWebDocument(
        url="https://telegra.ph/file/7fef8ad65d763c7a0df11.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    for result in results:
        title = str(((result.find("a")["href"]).replace("title", "")).replace("/", ""))
        pop_result.append(
            await e.builder.article(
                title=result.text,
                description=title,
                text=result.text + "\nTitle ID: " + f"`{title}`",
                thumb=thumb,
                buttons=(
                    Button.switch_inline("Search Again", query="imdb ", same_peer=True),
                    Button.inline(result.text[:15], data="imdb_data_{}".format(title)),
                ),
            )
        )
    await e.answer(pop_result)


@Cquery(pattern="google ?(.*)")
async def google_search_(e):
    query = e.pattern_match.group(1)
    if not query:
        return
    url = f"https://www.google.com/search?&q={query}&num=8"
    usr_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/61.0.3163.100 Safari/537.36"
    }
    r = get(url, headers=usr_agent)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.findAll("div", attrs={"class": "g"})
    descs = soup.findAll("div", attrs={"class": "IsZvec"})
    x = -1
    pop_result = []
    thumb = InputWebDocument(
        url="https://telegra.ph/file/eed40eeca6518e556c045.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    for _x in results:
        x += 1
        link = (_x.find("a", href=True))["href"]
        name = _x.find("h3")
        if name:
            name = name.text
        if not link and name:
            return
        try:
            desc = descs[x].text
        except:
            desc = ""
        text = f"<b><a href='{link}'>{name}</a></b>\n<code>{desc}</code>"
        pop_result.append(
            await e.builder.article(
                title=str(name),
                description=str(desc),
                text=text,
                thumb=thumb,
                parse_mode="html",
                link_preview=False,
                buttons=Button.switch_inline(
                    "Search Again", query="google ", same_peer=True
                ),
            )
        )
    await e.answer(pop_result)


@Cquery(pattern="news ?(.*)")
async def google_news_(e):
    query = e.pattern_match.group(1)
    if not query:
        return
    gnews = GoogleNews(lang="en")
    gnews.get_news(query)
    results = gnews.results()
    if len(results) == 0:
        return await e.answer(
            [
                e.builder.article(
                    title="No Result found", text="No news found for your query."
                )
            ]
        )
    pop_result = []
    r = 0
    for _x in results:
        r += 1
        if r == 7:
            break
        text = f'[{_x.get("title")}]({_x.get("link")})'
        thumb = None
        if _x.get("img"):
            thumb = InputWebDocument(
                url=_x.get("img"),
                size=1423,
                mime_type="image/jpeg",
                attributes=[],
            )
        pop_result.append(
            await e.builder.article(
                title=_x.get("title"),
                description=_x.get("desc"),
                text=text,
                thumb=thumb,
                link_preview=True,
                buttons=Button.switch_inline(
                    "Search Again", query="news ", same_peer=True
                ),
            )
        )
    await e.answer(pop_result)


@Cquery(pattern="torrent ?(.*)")
async def pirate_bay_(e):
    Query = e.pattern_match.group(1)
    if not Query:
        return
    tpb = TPB("https://tpb.party")
    results = tpb.search(Query)
    if len(results) == 0:
        return await e.answer(
            [
                await e.builder.article(
                    title="No Result found", text="No torrents found for your query."
                )
            ]
        )
    pop_result = []
    _x = 0
    for x in results:
        _x += 1
        if _x == 10:
            break
        pop_result.append(await e.builder.article(title=str(x), text=str(x)))
    await e.answer(pop_result)
