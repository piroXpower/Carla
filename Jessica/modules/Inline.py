import random
from shutil import rmtree
from urllib.parse import quote

from bing_image_downloader import downloader
from bs4 import BeautifulSoup
from GoogleNews import GoogleNews
from PIL import Image, ImageDraw, ImageFont
from requests import get
from researchacademic import ResearchAcademic
from telethon import Button, events
from telethon.tl.types import InputWebDocument
from tpblite import TPB
from youtubesearchpython import SearchVideos

from .. import tbot
from ..events import Cinline, Cquery

whisper_db = {}


@tbot.on(events.InlineQuery(pattern=None))
async def nan(event):
    builder = event.builder
    text = event.text
    text = text.replace("@MissNeko_Bot", "")
    if not text == "":
        return
    icon = InputWebDocument(
        url="https://telegra.ph/file/ee773e55c2e839255107a.jpg",
        size=1142,
        mime_type="image/jpeg",
        attributes=[],
    )
    results = []
    title_1 = "Neko"
    des_1 = "Bot Info and status"
    content_1 = gen_status()
    result_1 = builder.article(
        title=title_1,
        description=des_1,
        text=content_1,
        thumb=icon,
    )
    result_2 = await gen_help(event, icon)
    results.append(result_1)
    results.append(result_2)
    await event.answer(results)


def gen_status():
    txt = "**Neko Info**:"
    txt += "\nServer: Heroku"
    txt += "\nDatabase: MongoDB"
    txt += "\nTelethon: 1.23"
    txt += "\nPython: 3.11"
    return txt


async def gen_help(event, thumb):
    b_q = [
        [
            Button.switch_inline("PyPi Search", query="pypi ", same_peer=True),
            Button.switch_inline("YouTube Search", query="yt ", same_peer=True),
        ],
        [
            Button.switch_inline("Google Search", query="google ", same_peer=True),
            Button.switch_inline("News Search", query="news ", same_peer=True),
        ],
        [
            Button.switch_inline("Torrent Search", query="torrent ", same_peer=True),
            Button.switch_inline("IMDb Search", query="imdb ", same_peer=True),
        ],
        [
            Button.switch_inline("Amazon Search", query="amazon ", same_peer=True),
            Button.switch_inline("Wiki Search", query="wiki ", same_peer=True),
        ],
        [
            Button.switch_inline("Geo Search", query="geo ", same_peer=True),
            Button.switch_inline("Insta Search", query="insta ", same_peer=True),
        ],
        [
            Button.switch_inline("Academic Search", query="sci ", same_peer=True),
            Button.switch_inline("Git Search", query="git ", same_peer=True),
        ],
        [
            Button.switch_inline("StackOFlow Search", query="sof ", same_peer=True),
        ],
        [
            Button.switch_inline("Wallpaper Search", query="wall ", same_peer=True),
        ],
    ]
    return await event.builder.article(
        title="Inline Query Help Menu.",
        description="Inline query help menu of neko chan.",
        text="Inline query Help Menu.",
        buttons=b_q,
        thumb=thumb,
    )


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
        content = "**Send whisper messages through inline mode**\n\nUsage: `@Missneko_Bot [@username] text`"
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
    image = Image.open("neko/modules/sql/IMG_20210705_134908_649.jpg")
    font = ImageFont.truetype(
        "neko/modules/sql/FontsFree-Net-Ambiguity-radical.ttf", 70
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
        return await e.answer(
            [],
            switch_pm="IMDb Search. Enter your query",
            switch_pm_param="inline_imdb",
        )
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
                    Button.inline(result.text[:20], data="imdb_data_{}".format(title)),
                ),
            )
        )
    await e.answer(pop_result)


@Cinline(pattern="imdb_data(\_(.*))")
async def imdb_data_(e):
    title = ((e.pattern_match.group(1)).decode()).split("_", 1)[1]
    url = f"https://m.imdb.com/title/{title}"
    q = get(url)
    soup = BeautifulSoup(q.text, "html.parser")
    img = soup.find("meta", attrs={"property": "twitter:image"})
    if img:
        img = img.get("content")
    rating = (
        soup.find(
            "span",
            attrs={"class": "AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"},
        )
    ).text or 0
    title = (soup.find("meta", attrs={"property": "twitter:title"})).get("content")
    desc = (soup.find("meta", attrs={"property": "twitter:description"})).get("content")
    genre = soup.findAll("span", attrs={"class": "ipc-chip__text"})
    genr_e = "\n**Genre:**"
    for x in range(0, 3):
        if x != 2:
            genr_e += " " + genre[x].text + ","
        if x == 2:
            genr_e += " " + genre[x].text
    text = f"**[{title}]**({img})\n**Ratings:** `{rating}/10`{genr_e}\n\n`{desc}`"
    await e.edit(
        text,
        link_preview=True,
        buttons=Button.switch_inline("Search Again", query="imdb ", same_peer=True),
    )


@Cquery(pattern="google ?(.*)")
async def google_search_(e):
    query = e.pattern_match.group(1)
    if not query:
        return await e.answer(
            [],
            switch_pm="Google Search. Enter your query",
            switch_pm_param="inline_google",
        )
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
    thumb = InputWebDocument(
        url="https://telegra.ph/file/08156ae8095691e54dc6e.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    if not query:
        return await e.answer(
            [
                await e.builder.article(
                    title="Google News Search",
                    description="Enter a News query to search.",
                    text="no query was given!",
                    thumb=thumb,
                    buttons=Button.switch_inline(
                        "Search Again", query="news ", same_peer=True
                    ),
                )
            ],
            switch_pm="News Search",
            switch_pm_param="inline_news",
        )
    gnews = GoogleNews(lang="en")
    gnews.get_news(query)
    results = gnews.results()
    if len(results) == 0:
        return await e.answer(
            [
                e.builder.article(
                    title="No Result found",
                    text="No news found for your query.",
                    thumb=thumb,
                    buttons=Button.switch_inline(
                        "Search Again", query="news ", same_peer=True
                    ),
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
    thumb = InputWebDocument(
        url="https://telegra.ph/file/777136a6709b153cd3f9e.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    thumb2 = InputWebDocument(
        url="https://telegra.ph/file/ff27836d89ada8b928588.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    if not Query:
        return await e.answer(
            [
                await e.builder.article(
                    title="Pirate bay Search",
                    description="Enter a query to search.",
                    text="no search query was given!",
                    thumb=thumb2,
                    buttons=Button.switch_inline(
                        "Search Again", query="torrent ", same_peer=True
                    ),
                )
            ],
            switch_pm="Torrent search",
            switch_pm_param="inline_torrent",
        )
    tpb = TPB("https://tpb.party")
    results = tpb.search(Query)
    if len(results) == 0:
        return await e.answer(
            [
                await e.builder.article(
                    title="No Result found",
                    text="No torrents found for your query.",
                    buttons=Button.switch_inline(
                        "Search Again", query="torrent ", same_peer=True
                    ),
                )
            ]
        )
    pop_result = []
    _x = 0
    for x in results:
        _x += 1
        if _x == 10:
            break
        desc = f"Seeds: {x.seeds}\nLeeches: {x.leeches}\n{x.filesize}"
        text = f"Title: **{x.title}**\nSeeds: **{x.seeds}**\nLeeches: **{x.leeches}**\nMagnet: `{x.magnetlink}`"
        pop_result.append(
            await e.builder.article(
                title=x.title,
                description=desc,
                text=text,
                thumb=thumb,
                buttons=Button.switch_inline(
                    "Search Again", query="torrent ", same_peer=True
                ),
            )
        )
    await e.answer(pop_result)


@Cquery(pattern="wall ?(.*)")
async def wallpaper_search(e):
    q = e.pattern_match.group(1)
    if not q:
        return await e.answer(
            [
                await e.builder.article(
                    title="Wallpaper Search",
                    description="Enter a wall query to search.",
                    text="no query was given!",
                    thumb=None,
                    buttons=Button.switch_inline(
                        "Search Again", query="wall ", same_peer=True
                    ),
                )
            ],
            switch_pm="Wallpaper Search",
            switch_pm_param="inline_wall",
        )
    url = f"https://all-free-download.com/wallpapers/{q}.html"
    usr_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/61.0.3163.100 Safari/537.36"
    }
    r = get(url, headers=usr_agent)
    soup = BeautifulSoup(r.text, "html.parser")
    imgs = soup.find_all("div", attrs={"class": "item"})
    pops = []
    for x in imgs:
        img = x.find("a").find("img")
        src = img.get("src")
        if not src:
            return
        thumb = InputWebDocument(
            url=src,
            size=1423,
            mime_type="image/jpeg",
            attributes=[],
        )
        xrc = src.split("/")
        xname = xrc[len(xrc) - 1]
        name = img.get("alt") or "WallPaper"
        pops.append(
            await e.builder.article(
                title=name,
                thumb=thumb,
                text=f"[{name}]({src})",
                buttons=[
                    [
                        Button.switch_inline(
                            "Search Again", query="wall ", same_peer=True
                        )
                    ],
                    [
                        Button.inline(
                            "Generate HD Wallpaper", data="gen_hd_{}".format(xname)
                        )
                    ],
                ],
            )
        )
        if len(pops) == 6:
            break
    await e.answer(pops, gallery=True)


@Cinline(pattern="gen_hd(\_(.*))")
async def imdb_data_(e):
    ((e.pattern_match.group(1)).decode()).split("_", 1)[1]
    await e.answer("soon", alert=True)


@Cquery(pattern="amazon ?(.*)")
async def amazon_search(e):
    q = e.pattern_match.group(1)
    if not q:
        return await e.answer(
            [
                await e.builder.article(
                    title="Amazon Search",
                    description="Enter a query to search.",
                    text="no query was given!",
                    thumb=None,
                    buttons=Button.switch_inline(
                        "Search Again", query="amazon ", same_peer=True
                    ),
                )
            ],
            switch_pm="Amazon Search",
            switch_pm_param="inline_amazon",
        )
    url = f"https://www.amazon.in/s?k={q}&ref=nb_sb_noss"
    usr_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/61.0.3163.100 Safari/537.36"
    }
    r = get(url, headers=usr_agent)
    soup = BeautifulSoup(r.content, "html.parser")
    results = soup.findAll(
        "div", attrs={"class": "a-section aok-relative s-image-fixed-height"}
    )
    stars = soup.findAll("span", attrs={"class": "a-icon-alt"})
    prices = soup.findAll("span", attrs={"data-a-color": "price"})
    rp = soup.findAll(
        "span", attrs={"class": "a-size-medium a-color-base a-text-normal"}
    )
    if not rp:
        return await e.answer(
            [
                await e.builder.article(
                    title="Amazon Search",
                    description="No result was found",
                    text="no Result was found!",
                    thumb=None,
                    buttons=Button.switch_inline(
                        "Search Again", query="amazon ", same_peer=True
                    ),
                )
            ],
            switch_pm="Amazon Search",
            switch_pm_param="inline_amazon",
        )
    pop = []
    _f = -1
    for x in rp:
        name = x.text
        _f += 1
        if len(pop) == 6:
            break
        try:
            _x = results[_f]
            _x = x.find("img")
            src = _x.get("src")
        except:
            src = None
        try:
            price = prices[_f].find("span", attrs={"class": "a-offscreen"})
        except:
            price = None
        if price:
            price = price.text
        try:
            star = stars[_f].text
        except:
            star = ""
        desc = f"price: {price}\n{star}"
        if not name:
            name = "product"
        if src:
            thumb = InputWebDocument(
                url=src,
                size=1423,
                mime_type="image/jpeg",
                attributes=[],
            )
        else:
            thumb = None
        text = f"**[{name}]**({src})\nPrice: `{price}`\n{star}"
        pop.append(
            await e.builder.article(
                title=name,
                description=desc,
                text=text,
                thumb=thumb,
                link_preview=True,
                buttons=Button.switch_inline(
                    "Search Again",
                    query="amazon ",
                    same_peer=True,
                ),
            )
        )
    await e.answer(pop)


@Cquery(pattern="wiki ?(.*)")
async def Wikipedia_search(e):
    q = e.pattern_match.group(1)
    thumb = InputWebDocument(
        url="https://telegra.ph/file/ca502b584b445fc985564.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    if not q:
        return await e.answer(
            [
                await e.builder.article(
                    title="Wikipedia Search",
                    description="Enter a query to search.",
                    text="no query was given!",
                    thumb=thumb,
                    buttons=Button.switch_inline(
                        "Search Again", query="wiki ", same_peer=True
                    ),
                )
            ],
            switch_pm="Wikipedia Search",
            switch_pm_param="inline_wiki",
        )
    url = "http://en.wikipedia.org/w/api.php"
    data = {
        "list": "search",
        "srprop": "",
        "srlimit": 5,
        "srsearch": q,
        "action": "query",
        "format": "json",
    }
    usr_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/61.0.3163.100 Safari/537.36"
    }
    r = get(url, params=data, headers=usr_agent)
    search = r.json().get("query").get("search")
    if len(search) == 0:
        return await e.answer(
            [
                await e.builder.article(
                    title="Wikipedia Search",
                    description="No result was found",
                    text="no Result was found!",
                    thumb=thumb,
                    buttons=Button.switch_inline(
                        "Search Again", query="wiki ", same_peer=True
                    ),
                )
            ],
            switch_pm="Wikipedia Search",
            switch_pm_param="inline_wiki",
        )
    final_pop = []
    for _x in search:
        header = _x.get("title")
        page_header = header.replace(" ", "_")
        page_url = "https://en.wikipedia.org/wiki/{}".format(page_header)
        final_pop.append(
            await e.builder.article(
                thumb=thumb,
                title=header,
                text=f"<b><a href='{page_url}'>{header}</a></b>",
                parse_mode="html",
            )
        )
    await e.answer(final_pop)


@Cquery(pattern="img ?(.*)")
async def image_search(e):
    q = e.pattern_match.group(1)
    if not q:
        return
    downloader.download(
        q,
        limit=3,
        output_dir="dataset",
        adult_filter_off=False,
        force_replace=False,
        timeout=60,
        verbose=False,
    )
    pp = []
    i = 0
    for x in range(0, 3):
        i += 1
        path = f"dataset/{q}/Image_{i}.jpg"
        pp.append(await e.builder.photo(path))
    await e.answer(pp, gallery=True)
    rmtree(f"dataset/{q}")


@Cquery(pattern="geo ?(.*)")
async def geo_search_(e):
    q = e.pattern_match.group(1)
    if not q:
        return
    thumb = InputWebDocument(
        url="https://telegra.ph/file/da565819d3f99e43fecec.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    url = f"http://dev.virtualearth.net/REST/v1/Autosuggest?query={q}&key=AsVuFq5LexGs3arw0czJopBSoYAdCuJroMLXnAa7SugcRjR1ulFGikBR-DYOcxs2"
    r = get(url)
    try:
        r = r.json().get("resourceSets")[0].get("resources")[0].get("value")
    except (IndexError, KeyError):
        return
    c = ["1", "2", "3", "4", "5"]
    pop_list = []
    for x in r:
        if len(pop_list) == 5:
            break
        pic_link = f"https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/{quote(q)}?mapSize=500,500&key=AsVuFq5LexGs3arw0czJopBSoYAdCuJroMLXnAa7SugcRjR1ulFGikBR-DYOcxs2"
        a = x.get("address")
        title = a.get("locality")
        description = a.get("formattedAddress")
        text = f"**[{description}]**({pic_link})\n**Locality:** {title}\n**State:** {a.get('adminDistrict')}\n**Country:** {a.get('countryRegion')}, {a.get('countryRegionIso2')}"
        pop_list.append(
            await e.builder.article(
                title=str(c[len(pop_list)]) + ". " + str(title),
                description=str(description),
                text=text,
                thumb=thumb,
                link_preview=True,
                buttons=[
                    [Button.inline(title or "Map", data=f"geo_{description[:30]}")],
                    [
                        Button.switch_inline(
                            "Search Again", query="geo ", same_peer=True
                        )
                    ],
                ],
            )
        )
    await e.answer(pop_list)


@Cquery(pattern="insta ?(.*)")
async def instagram_search_(e):
    q = e.pattern_match.group(1)
    if not q:
        return
    url = f"https://gramho.com/search/{q}"
    usr_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/61.0.3163.100 Safari/537.36"
    }
    r = get(url, headers=usr_agent)
    soup = BeautifulSoup(r.content, "html.parser")
    results = soup.findAll("div", attrs={"class": "result-username"})
    answers = []
    urls = soup.find("div", attrs={"class": "search-results"})
    url_ss = urls.find_all("a", href=True)
    images = soup.find_all("img")
    q = -1
    for x in results:
        q += 1
        username = x.text
        url = url_ss[q]["href"]
        insta_url = f"www.instagram.com/{username}/"
        text = f"**[{username}]**({url})"
        try:
            img = images[q]
        except IndexError:
            img = None
        if img:
            img_url = "https://gramho.com/" + img.get("src")
            thumb = InputWebDocument(
                url=img_url,
                size=1423,
                mime_type="image/jpeg",
                attributes=[],
            )
        else:
            pass
        answers.append(
            await e.builder.article(
                title=username,
                description=insta_url,
                text=text,
                thumb=thumb,
                link_preview=True,
                buttons=[
                    [Button.inline(username, data=f"i_click_{username}")],
                    [
                        Button.switch_inline(
                            "Search Again", query="insta ", same_peer=True
                        )
                    ],
                ],
            )
        )
        if len(answers) == 30:
            break
    await e.answer(answers)


@Cinline(pattern="i_click(\_(.*))")
async def imdb_data_(e):
    q = ((e.pattern_match.group(1)).decode()).split("_", 1)[1]
    url = f"https://gramho.com/search/{q}"
    usr_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/61.0.3163.100 Safari/537.36"
    }
    qr = q.replace("@", "")
    r = get(url, headers=usr_agent)
    old_soup = BeautifulSoup(r.content, "html.parser")
    rq_url = (old_soup.find("div", attrs={"class": "search-results"})).find_all(
        "a", href=True
    )[0]["href"]
    r_new = get(rq_url, headers=usr_agent)
    soup = BeautifulSoup(r_new.content, "html.parser")
    description = soup.find("div", attrs={"class": "profile-description"})
    if description:
        description = description.text
    else:
        description = ""
    img = soup.findAll("img")
    if img and img[1]:
        img = "https://gramho.com/" + img[1].get("src")
    else:
        img = ""
    name = soup.find("h2", attrs={"class": "profile-name-bottom"}).text or "User"
    posts = soup.findAll("span", attrs={"class": "black-box"})[0].text
    followers = soup.findAll("span", attrs={"class": "bold"})[0].text
    following = soup.findAll("span", attrs={"class": "bold"})[1].text
    final_text = f"**[{name}]**({img})\n__{q}__\nAbout: {description}\n\n**{followers}**, **{following}**, **{posts}**"
    await e.edit(
        final_text,
        link_preview=True,
        buttons=[
            [Button.url(name or "View User", "https://instagram.com/{}".format(qr))],
            [Button.switch_inline("Search Again", query="insta ", same_peer=True)],
        ],
    )


@Cquery(pattern="sci ?(.*)")
async def sci_search_(e):
    q = e.pattern_match.group(1)
    if not q:
        return
    AZURE_ACADEMIC_API_KEY = "131fe05ff0a7435a94e2585800951fa0"
    r = ResearchAcademic(AZURE_ACADEMIC_API_KEY)
    results = r.evaluate(q, timeout=5)
    if len(results) == 0:
        return
    final_a = []
    thumb = InputWebDocument(
        url="https://telegra.ph/file/dfce1c97abc872bf51cbc.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    for _x in results:
        title = _x.get("title") or "Project_"
        abstract = _x.get("abstract")
        if len(abstract) > 1024:
            abstract = abstract[:1024]
        authors = ""
        for au in _x.get("authors"):
            authors += " " + au.get("name") or ""
        if _x.get("journal"):
            book = _x.get("journal").get("name")
        else:
            book = ""
        year = _x.get("year") or ">2010"
        text = f"**{title}**\n**Authors**: {authors}\n**Journel:** {book}\n**Released:** {year}\n\n`{abstract}`"
        description = f"Year: {year}\n{authors}\n{book}"
        final_a.append(
            await e.builder.article(
                title=title,
                description=description,
                text=text,
                parse_mode="md",
                thumb=thumb,
                link_preview=False,
                buttons=Button.switch_inline(
                    "Search Again", query="sci ", same_peer=True
                ),
            )
        )
    await e.answer(final_a)


@Cquery(pattern="git ?(.*)")
async def git_search_(e):
    thumb = InputWebDocument(
        url="https://telegra.ph/file/08c929fec4c35236b696c.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    q = e.pattern_match.group(1)
    if not q:
        return await e.answer(
            [
                await e.builder.article(
                    title="GitHub Search",
                    description="Enter a query to search.",
                    text="no query was given!",
                    thumb=thumb,
                    buttons=Button.switch_inline(
                        "Search Again", query="git ", same_peer=True
                    ),
                )
            ],
            switch_pm="Gthub Search",
            switch_pm_param="inline_git",
        )
    url = "https://github.com/search?q={}&type=".format(q)
    r = get(url)
    soup = BeautifulSoup(r.content, "lxml")
    repos = soup.find_all("div", attrs={"class": "mt-n1"})
    langs = soup.find_all("span", attrs={"itemprop": "programmingLanguage"})
    ds = soup.findAll("p", attrs={"class": "mb-1"})
    if len(repos) == 0:
        return await e.answer(
            [
                await e.builder.article(
                    title="GitHub Search",
                    description="No result was found",
                    text="No result was found!",
                    thumb=thumb,
                    buttons=Button.switch_inline(
                        "Search Again", query="git ", same_peer=True
                    ),
                )
            ],
            switch_pm="Gthub Search",
            switch_pm_param="inline_git",
        )
    pop = []
    x = 0
    for _x in repos:
        if len(pop) == 5:
            break
        author, repo = _x.find("a").text.split("/", 1)
        try:
            lang = langs[x].text
        except IndexError:
            lang = ""
        try:
            description = ds[x].text
        except IndexError:
            description = lang
        x += 1
        text = "<u><b><a href='https://github.com/{}/{}'>{}</a></b></u>\nLang: <b>{}</b>\nAuthor: <b>{}</b>\n<code>{}</code>".format(
            author.strip(),
            repo.strip(),
            repo.strip(),
            lang,
            author.strip(),
            description,
        )
        pop.append(
            await e.builder.article(
                title=repo.strip(),
                description=description,
                text=text,
                link_preview=False,
                thumb=thumb,
                parse_mode="html",
                buttons=[
                    [
                        Button.url(
                            author.strip() + ", " + repo.strip(),
                            "https://github.com/{}/{}".format(
                                author.strip(), repo.strip()
                            ),
                        )
                    ],
                    [
                        Button.switch_inline(
                            "Search Again", query="git ", same_peer=True
                        )
                    ],
                ],
            )
        )
    await e.answer(pop)


@Cquery(pattern="steam ?(.*)")
async def fit_girl_search_(e):
    q = e.pattern_match.group(1)
    if not q:
        return
    q = q.replace(" ", "+")
    url = f"https://store.steampowered.com/search/?term={q}"
    r = get(url)
    soup = BeautifulSoup(r.content, "lxml")
    titles = soup.find_all("span", attrs={"class": "title"})
    if len(titles) == 0:
        return
    prices = soup.findAll(
        "div", attrs={"class": "col search_price responsive_secondrow"}
    )
    reviews = soup.find_all("span", attrs={"class": "search_review_summary positive"})
    images = soup.find_all("div", attrs={"class": "col search_capsule"})
    pop = []
    x = 0
    for _x in titles:
        if len(pop) == 10:
            break
        title = _x.text
        price = prices[x].text
        review = reviews[x].get("data-tooltip-html")
        if review:
            review = review.replace("<br>", "")
        image = images[x].find("img").get("src")
        thumb = None
        if image:
            thumb = InputWebDocument(
                url=image,
                size=1423,
                mime_type="image/jpeg",
                attributes=[],
            )
            text = f"**{title}**" + f"\nPrice: {price}"
            pop.append(
                await e.builder.article(
                    title=title,
                    description=review,
                    text=text,
                    link_preview=False,
                    thumb=thumb,
                    parse_mode="md",
                    buttons=[
                        [
                            Button.url(title, "https://steam.com"),
                        ],
                        [
                            Button.switch_inline(
                                "Search Again", query="steam ", same_peer=True
                            )
                        ],
                    ],
                )
            )
    await e.answer(pop)


@Cquery(pattern="gay ?(.*)")
async def how_gey_(e):
    q = e.pattern_match.group(1)
    if not q:
        name = e.sender.first_name
    else:
        name = q
    percentage = str(random.randint(0, 100)) + "%"
    if not q:
        text = "🏳️‍🌈 I am {} gay!".format(percentage)
        title = "🏳️‍🌈 How gay are you?"
        d = "Send your current gayness to this chat."
    else:
        text = "🏳️‍🌈 {} is {} gay!".format(name, percentage)
        title = "🏳️‍🌈 How gay is {}?".format(name)
        d = "Send {}'s gayness to this chat.".format(name)
    buttons = Button.switch_inline(
        "Share your gayness! 🏳️‍🌈", query="gay ", same_peer=False
    )
    thumb = InputWebDocument(
        url="https://telegra.ph/file/7aab1996da5c88f7d1b5e.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    await e.answer(
        [
            e.builder.article(
                title=title,
                text=text,
                description=d,
                thumb=thumb,
                parse_mode="html",
                buttons=buttons,
            )
        ]
    )


@Cquery(pattern="sof ?(.*)")
async def stack_overflow_search__(e):
    q = e.pattern_match.group(1)
    if not q:
        return
    q = quote(q)
    url = "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=relevance&q={}&accepted=True&site=stackoverflow".format(
        q
    )
    r = get(url)
    try:
        r = r.json().get("items")
    except:
        return
    if len(r) == 0:
        return
    pop = []
    q = 0
    for x in r:
        q += 1
        title = x.get("title")
        tgs = x.get("tags")
        link = x.get("link")
        view_count = x.get("view_count")
        author = x.get("display_name")
        img = x.get("profile_image")
        tags = ""
        for x in tgs:
            tags += str(x) + " "
        if img:
            thumb = InputWebDocument(
                url=img,
                size=1423,
                mime_type="image/jpeg",
                attributes=[],
            )
        else:
            thumb = None
        pop.append(
            await e.builder.article(
                title=title or "{}.stackoverflow".format(q),
                description=str(tags) + "\nPosted by: {}".format(author),
                text=str(link) + str(view_count),
                thumb=thumb,
                buttons=Button.switch_inline(
                    "Search Again", query="sof ", same_peer=True
                ),
            )
        )
    await e.answer(pop)
