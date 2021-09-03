import re
from os import remove
from random import randint

import bs4
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from geopy.geocoders import Nominatim
from requests import get, post, request
from telethon.tl.types import InputGeoPoint, InputMediaDice, InputMediaGeoPoint

from neko import tbot, ubot
from neko.modules.sql.nightmode_sql import (
    add_nightmode,
    get_all_chat_id,
    is_nightmode_indb,
    rmnightmode,
)
from neko.utils import Cbot

from . import can_change_info

enable = ["enable", "on", "y", "yes"]
disable = ["disable", "off", "n" "no"]


@Cbot(pattern="^/nightmode ?(.*)")
async def lilz(event):
    if event.is_private:
        return
    if not await can_change_info(event, event.sender_id):
        return
    args = event.pattern_match.group(1)
    if not args:
        if is_nightmode_indb(event.chat_id):
            await event.reply("**NightMode** is currently **enabled** for this chat.")
        else:
            await event.reply("**NightMode** is currently **disabled** for this chat.")
    elif args in enable:
        await event.reply(
            "Enabled nightmode for this.\n\nGroup closes at 12Am and opens at 6Am IST"
        )
        add_nightmode(event.chat_id)
    elif args in disable:
        await event.reply("Disabled nightmode for this chat.")
        rmnightmode(event.chat_id)


async def job_close():
    nt_chats = get_all_chat_id()
    if len(nt_chats) == 0:
        return
    for chats in nt_chats:
        try:
            await tbot.send_message(
                int(chats.chat_id),
                "12:00 Am, Group Is Closing Till 6 Am. Night Mode Started ! \n**Powered By neko**",
            )
            await tbot.edit_permissions(int(chats.chat_id), send_messages=False)
        except Exception as e:
            logger.info(f"Unable To Close Group {chats.chat_id} - {e}")


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hour=23, minute=58)
scheduler.start()


async def job_open():
    nt_chats = get_all_chat_id()
    if len(nt_chats) == 0:
        return
    for chats in nt_chats:
        try:
            await tbot.send_message(
                int(chats.chat_id),
                "06:00 Am, Group Is Opening.\n**Powered By neko**",
            )
            await tbot.edit_permissions(int(chats.chat_id), send_messages=True)
        except Exception as e:
            logger.info(f"Unable To Open Group {chats.chat_id} - {e}")


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_open, trigger="cron", hour=6, minute=1)
scheduler.start()


@Cbot(pattern="^/(GitHub|github) ?(.*)")
async def gt(event):
    arg = event.pattern_match.group(2)
    git = get(f"https://api.github.com/users/{arg}").json()
    try:
        fileid = git["avatar_url"]
    except KeyError:
        fileid = None
    try:
        if git["type"] == "User":
            text = "<b>User Info:</b>"
        else:
            text = "<b>Organization Info:</b>"
    except KeyError:
        pass
    try:
        name = git["name"]
        text += f"\n<b>Name:</b> {name}"
    except KeyError:
        pass
    try:
        id = git["id"]
        text += f"\n<b>ID:</b> <code>{id}</code>"
    except KeyError:
        pass
    try:
        nid = git["node_id"]
        text += f"\n<b>Node ID:</b> {nid}"
    except KeyError:
        pass
    try:
        company = git["company"]
        if not company == None:
            text += f"\n<b>Company:</b> {company}"
    except KeyError:
        pass
    try:
        followers = git["followers"]
        if not followers == None:
            text += f"\n<b>Followers:</b> {followers}"
    except KeyError:
        pass
    try:
        blog = git["blog"]
        if not blog == None:
            text += f"\n<b>Blog:</b> <code>{blog}</code>"
    except KeyError:
        pass
    try:
        location = git["location"]
        if not location == None:
            text += f"\n<b>Location:</b> {location}"
    except KeyError:
        pass
    try:
        bio = git["bio"]
        if not bio == None:
            text += f"\n\n<b>Bio:</b> <code>{bio}</code>"
    except KeyError:
        pass
    try:
        twitter = git["twitter_username"]
        if not twitter == None:
            text += f"\n\n<b>Twitter:</b> {twitter}"
    except KeyError:
        pass
    try:
        email = git["email"]
        if not email == None:
            text += f"\n<b>Email:</b> <code>{email}</code>"
    except KeyError:
        pass
    try:
        repo = git["public_repos"]
        text += f"\n<b>Repos:</b> {repo}"
    except KeyError:
        pass
    try:
        url = git["html_url"]
        text += f"\n\n<b>URL:</b> <code>{url}</code>"
    except KeyError:
        pass
    await event.respond(text, parse_mode="html", file=fileid)


@Cbot(pattern="^/repo ?(.*)")
async def lo(event):
    if (
        event.text.startswith("!report")
        or event.text.startswith("?report")
        or event.text.startswith("/report")
    ):
        return
    arg = event.pattern_match.group(1)
    usr = get(f"https://api.github.com/users/{arg}/repos?per_page=40").json()
    reply_text = "<b>Repo:</b>"
    for i in range(len(usr)):
        reply_text += f'\n<a href="{usr[i]["html_url"]}">{usr[i]["name"]}</a>'
    await event.respond(reply_text, parse_mode="htm", link_preview=False)


@Cbot(pattern="^/imdb ?(.*)")
async def imdb(e):
    try:
        movie_name = e.pattern_match.group(1)
        remove_space = movie_name.split(" ")
        final_name = "+".join(remove_space)
        page = get("https://www.imdb.com/find?ref_=nv_sr_fn&q=" + final_name + "&s=all")
        str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, "lxml")
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext("td").findNext("td").text
        mov_link = (
            "http://www.imdb.com/" + odds[0].findNext("td").findNext("td").a["href"]
        )
        page1 = get(mov_link)
        soup = bs4.BeautifulSoup(page1.content, "lxml")
        if soup.find("div", "poster"):
            poster = soup.find("div", "poster").img["src"]
        else:
            poster = ""
        if soup.find("div", "title_wrapper"):
            pg = soup.find("div", "title_wrapper").findNext("div").text
            mov_details = re.sub(r"\s+", " ", pg)
        else:
            mov_details = ""
        credits = soup.findAll("div", "credit_summary_item")
        if len(credits) == 1:
            director = credits[0].a.text
            writer = "Not available"
            stars = "Not available"
        elif len(credits) > 2:
            director = credits[0].a.text
            writer = credits[1].a.text
            actors = []
            for x in credits[2].findAll("a"):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        else:
            director = credits[0].a.text
            writer = "Not available"
            actors = []
            for x in credits[1].findAll("a"):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        if soup.find("div", "inline canwrap"):
            story_line = soup.find("div", "inline canwrap").findAll("p")[0].text
        else:
            story_line = "Not available"
        info = soup.findAll("div", "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll("a")
                for i in a:
                    if "country_of_origin" in i["href"]:
                        mov_country.append(i.text)
                    elif "primary_language" in i["href"]:
                        mov_language.append(i.text)
        if soup.findAll("div", "ratingValue"):
            for r in soup.findAll("div", "ratingValue"):
                mov_rating = r.strong["title"]
        else:
            mov_rating = "Not available"
        file = None
        if poster:
            file = poster
        await e.reply(
            "<b>Title : </b><code>"
            + mov_title
            + "</code>\n<code>"
            + mov_details
            + "</code>\n<b>Rating : </b><code>"
            + mov_rating
            + "</code>\n<b>Country : </b><code>"
            + mov_country[0]
            + "</code>\n<b>Language : </b><code>"
            + mov_language[0]
            + "</code>\n<b>Director : </b><code>"
            + director
            + "</code>\n<b>Writer : </b><code>"
            + writer
            + "</code>\n<b>Stars : </b><code>"
            + stars
            + "</code>\n<b>IMDB Url : </b>"
            + mov_link
            + "\n<b>Story Line : </b>"
            + story_line[:40],
            link_preview=True,
            parse_mode="HTML",
            file=file,
            force_document=True,
        )
    except Exception as k:
        await e.reply(str(k))
    except IndexError:
        await e.reply("Please enter a valid movie name !")


@Cbot(pattern="^/math ?(.*)")
async def ss(event):
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await event.reply("Please provide the Mathamatical Equation.")
    url = "https://evaluate-expression.p.rapidapi.com/"
    querystring = {"expression": input_str}
    headers = {
        "x-rapidapi-key": "fef481fee3mshf99983bfc650decp104100jsnbad6ddb2c846",
        "x-rapidapi-host": "evaluate-expression.p.rapidapi.com",
    }
    response = request("GET", url, headers=headers, params=querystring)
    if not response or not response.text:
        return await event.reply("Invalid Mathamatical Equation provided.")
    await event.reply(response.text)


@Cbot(pattern="^/shazam$")
async def az(event):
    if not event.reply_to_msg_id:
        return await event.reply("Reply to an audio file to recognise it!")
    msg = await event.get_reply_message()
    if not msg.audio and not msg.video:
        return await event.reply("This replied file is not an audio or video!")
    stt = await event.reply("Identifying the song...")
    tmp = "./"
    dl = await tbot.download_media(msg, tmp)
    async with ubot.conversation("@auddbot") as conv:
        await conv.send_file(dl)
        check = await conv.get_response()
        if not check.text.startswith("Audio received"):
            return await stt.edit(
                "An error while identifying the song. Try to use a 5-10s long audio message."
            )
        await stt.edit("Wait just a sec...")
        result = await conv.get_response()
        await ubot.send_read_acknowledge(conv.chat_id)
    namem = f"Song Name : {result.text.splitlines()[0]}\
        \n\nDetails : {result.text.splitlines()[2]}[.]({result.text.splitlines()[4]})"
    await stt.edit(namem, link_preview=True)


@Cbot(pattern="^/(color|Color|Colour|colour)")
async def colt(e):
    api_key = "58199388-5499-4c98-b052-c679b16310f9"
    if not e.reply_to_msg_id:
        return await e.reply("Reply to an Image to add color to it!")
    elif e.reply_to_msg_id:
        file = await e.get_reply_message()
        if not file.sticker and not file.photo:
            return await e.reply(
                "That's not an image, please reply to an Image to add color to it!"
            )
        ud = await e.reply("**Colourizing** the image...")
        media = await tbot.download_media(file)
        r = post(
            "https://api.deepai.org/api/colorizer",
            files={
                "image": open(media, "rb"),
            },
            headers={"api-key": api_key},
        )
    remove(media)
    if "status" in r.json():
        return await ud.edit(r.json()["status"])
    r_json = r.json()["output_url"]
    await tbot.send_file(e.chat_id, file=str(r_json), force_document=False)
    await ud.delete()


@Cbot(pattern="^/gps ?(.*)")
async def gps(event):
    args = event.pattern_match.group(1)
    if not args:
        return await event.reply("Enter some location to get its position!")
    try:
        geolocator = Nominatim(user_agent="SkittBot")
        location = args
        geoloc = geolocator.geocode(location)
        longitude = geoloc.longitude
        latitude = geoloc.latitude
        gm = "https://www.google.com/maps/search/{},{}".format(latitude, longitude)
        await event.respond(
            "Open with: [Google Maps]({})".format(gm),
            file=InputMediaGeoPoint(InputGeoPoint(float(latitude), float(longitude))),
            link_preview=False,
        )
    except Exception as e:
        await event.reply("Unable to locate that place. " + str(e))


"""
@tbot.on.utils.InlineQuery)
async def handler(event):
                        builder = event.builder
                        rev_text = event.text[::-1]
                        await event.answer([
                            builder.article('Reverse text', text=rev_text)], switch_pm="hi babe", switch_pm_param="help")
"""


@Cbot(pattern="^/pypi ?(.*)")
async def pi(event):
    args = event.pattern_match.group(1)
    if not args:
        return await event.reply(
            "Please input the name of a pypi library to gather it's info."
        )
    url = f"https://pypi.org/pypi/{args}/json"
    response = get(url)
    if not response:
        return await event.reply("Invalid pypi package provided!")
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
    await event.respond(py, parse_mode="htm")


@Cbot(pattern="^/(jackpot|dice|dart|goal|football|basketball|bowling)$")
async def dart(event):
    args = event.pattern_match.group(1)
    if not args:
        return
    if args == "jackpot":
        await event.respond(file=InputMediaDice("🎰"))
    elif args == "dice":
        await event.respond(file=InputMediaDice("🎲"))
    elif args == "dart":
        await event.respond(file=InputMediaDice("🎯"))
    elif args in ["goal", "football"]:
        await event.respond(file=InputMediaDice("⚽"))
    elif args == "basketball":
        await event.respond(file=InputMediaDice("🏀"))
    elif args == "bowling":
        await event.respond(file=InputMediaDice("🎳"))


@Cbot(pattern="^/(crypto|btc|Crypto|BTC|Btc|ETH|Eth|eth|DOGE|Doge|doge|ltc)$")
async def kek(event):
    url = "http://api.coinlayer.com/live"
    params = {"access_key": "7029df83c8dd41e61faa6d61d8846d05"}
    chart = get(url, params=params)
    btc = chart.json()["rates"]["BTC"]
    ltc = chart.json()["rates"]["LTC"]
    doge = chart.json()["rates"]["DOGE"]
    eth = chart.json()["rates"]["ETH"]
    valid = "<b>Crypto Prices:</b>"
    valid += f"\n\n<b><i>BTC:</i></b> <code>{btc}$</code>"
    valid += f"\n<b><i>LTC:</i></b> <code>{ltc}$</code>"
    valid += f"\n<b><i>DOGE:</i></b> <code>{doge}$</code>"
    valid += f"\n<b><i>ETH:</i></b> <code>{eth}$</code>"
    await event.reply(
        valid,
        parse_mode="htm",
    )


@Cbot(pattern="^/(yts|movie|Yts|Movie) ?(.*)")
async def _(event):
    if not event.pattern_match.group(2):
        return await event.reply("Please enter the M∆vie Name.")
    movie = event.pattern_match.group(2)
    url = f"http://www.omdbapi.com/?apikey=b8c61fb0&t={movie}"
    result = get(url)
    if not result:
        return
    result = result.json()
    text = ""
    try:
        title = result["Title"]
        text += f"<b>Title:</b> {title}"
    except KeyError:
        pass
    try:
        year = result["Year"]
        text += f"\n<b>Year:</b> {year}"
    except KeyError:
        pass
    try:
        rated = result["Rated"]
        text += f"\n<b>Rated:</b> {rated}"
    except KeyError:
        pass
    try:
        file = result["Poster"]
    except KeyError:
        file = None
    try:
        genre = result["Genre"]
        text += f"\n<b>Genre:</b> {genre}"
    except KeyError:
        pass
    try:
        release = result["Released"]
        text += f"\n<b>Released:</b> {release}"
    except KeyError:
        pass
    try:
        director = result["Director"]
        text += f"\n<b>Director:</b> {director}"
    except KeyError:
        pass
    try:
        box = result["BoxOffice"]
        text += f"\n<b>BoxOffice:</b> <code>{box}</code>"
    except KeyError:
        pass
    try:
        pro = result["Production"]
        text += f"\n<b>Production:</b> {pro}"
    except KeyError:
        pass
    try:
        plot = result["Plot"]
        text += f"\n\n<b>Story:</b> <i>{plot}</i>"
    except KeyError:
        pass
    try:
        langvaze = result["Languages"]
        text += f"\n\n<b>Languages:</b> <i>{langvaze}</i>"
    except KeyError:
        pass
    try:
        rate = result["Ratings"]
        text += "\n\n<b><u>Ratings:</u></b>"
        for i in rate:
            src = i["Source"]
            rating = i["Value"]
            text += f"\n<b>{src}</b>: <code>{rating}</code>"
    except KeyError:
        pass
    await event.reply(text, file=file, parse_mode="html", force_document=True)


@Cbot(pattern="^/stt$")
async def b(event):
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        if not reply_msg.media:
            return await event.reply(
                "Reply to a voice message, to get the text out of it."
            )
    else:
        return await event.reply("Reply to a voice message, to get the text out of it.")
    audio = await tbot.download_media(reply_msg, "./")
    kek = await event.reply("Starting Analysis...")
    headers = {
        "Content-Type": reply_msg.media.document.mime_type,
    }
    data = open(audio, "rb").read()
    response = post(
        "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/d5d8fabf-bbc8-4c2d-8575-36638227a70e"
        + "/v1/recognize",
        headers=headers,
        data=data,
        auth=("apikey", "04WmiAo7b-cDJvAimSLMlnWGiyl1OPoRCOeE_wiS2WAz"),
    )
    response = response.json()
    if "results" in response:
        results = response["results"]
        transcript_response = ""
        transcript_confidence = ""
        for alternative in results:
            alternatives = alternative["alternatives"][0]
            transcript_response += " " + str(alternatives["transcript"])
            transcript_confidence += " " + str(alternatives["confidence"]) + " + "
        if transcript_response != "":
            string_to_show = "TRANSCRIPT: __{}__\nConfidence: `{}`".format(
                transcript_response, transcript_confidence
            )
        else:
            string_to_show = "TRANSCRIPT: `Nil`\n\n**No Results Found**"
        await kek.edit(string_to_show)
    else:
        await event.reply(response["error"])
    remove(required_file_name)


@Cbot(pattern="^/stickerid ?(.*)")
async def Sid(event):
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        return await event.reply("Please reply to a sticker message to get its id.")
    elif event.reply_to_msg_id:
        msg = await event.get_reply_message()
        if not msg.sticker:
            return await event.reply(
                "That's not a sticker! Reply to a sticker to obtain it's ID."
            )
        file_id = msg.file.id
        await event.reply(
            f"<b>Sticker ID:</b> <code>{file_id}</code>", parse_mode="html"
        )
    elif event.pattern_match.group(1):
        sticker_id = event.pattern_match.group(1)
        try:
            sticker = await event.reply(file=sticker_id)
        except ValueError:
            await event.reply(
                "Invalid BOT_FILE_ID provided, failed to convert given id to a media."
            )


@Cbot(pattern="^/(cc|gencc|gen) ?(.*)")
async def cc_gen(e):
    no_r = 3
    try:
        input = e.text.split(None, 1)[1]
    except IndexError:
        return await e.reply("Please provide the BIN to generate")
    if "-" in input and len(input.split("-", 1)) >= 2:
        no_r = input.split("-", 1)[1]
        input = input[: (len(input) - len(no_r))]
        if no_r.isdigit():
            no_r = int(no_r)
        else:
            no_r = 3
    input = input.replace(" -", "")
    input = input.replace("x", "")
    q = input.replace("|", "")
    print(q)
    if not q.isdigit():
        return await e.reply("number bej bmsdk")
    if no_r > 50:
        no_r = 50
    if "|" in input:
        x = input.split("|")
        if len(x) == 4:
            cc = x[0]
            mo = x[1]
            yr = x[2]
            cvv = x[3]
        elif len(x) == 3:
            cc = x[0]
            mo = x[1]
            yr = x[2]
            cvv = None
        elif len(x) == 2:
            cc = x[0]
            yr = None
            if len(x[1]) <= 2:
                mo = x[1]
                cvv = None
            else:
                mo = None
                cvv = x[1]
        else:
            cc = x[0]
            cvv = mo = yr = None
        if len(cvv) == 2:
            cvv = "0" + cvv
        elif len(cvv) == 1:
            cvv = "00" + cvv
    else:
        cc = input
        cvv = mo = yr = None
    cc_len = 16
    gen_len = cc_len - len(str(cc))
    final_t = f"**generated** for `{input}`:"
    for q in range(no_r):
        genn = cc
        for x in range(gen_len):
            genn += str(randint(0, 9))
        if not mo:
            month = str(randint(1, 12))
            if len(month) == 1:
                month = "0" + month
        else:
            month = mo
        if not yr:
            year = str(randint(22, 30))
        else:
            year = yr
        if not cvv:
            cvv2 = str(randint(10, 999))
        else:
            cvv2 = cvv
        if len(cvv2) == 2:
            cvv2 = "0" + cvv2
        final = genn + "|" + month + "|" + "20" + year + "|" + cvv2
        final_t += "\n" + f"`{final}`"
    await e.reply(final_t)
