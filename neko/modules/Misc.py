import asyncio
import json
import os
import random
import re
from datetime import datetime

try:
    import carbon
except:
    os.system("pip install py-carbon")
    import carbon

from bing_image_urls import bing_image_urls
from bs4 import BeautifulSoup
from geniuses import GeniusClient
from gpytranslate import SyncTranslator
from gtts import gTTS
from mutagen.mp3 import MP3
from PIL import Image
from requests import get, post
from telegraph import Telegraph, upload_file
from telethon import Button, types
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    Channel,
    DocumentAttributeAudio,
    MessageMediaDocument,
    PhotoEmpty,
    User,
)

from .. import BOT_ID, CMD_HELP, OWNER_ID, tbot
from ..utils import Cbot, Cinline
from . import DEVS, SUDO_USERS, db, get_user, human_format
from .mongodb.couples_db import (
    add_vote_down,
    add_vote_up,
    get_couple,
    rm_vote_down,
    rm_vote_up,
    save_couple,
    voted_down,
    voted_up,
)

gbanned = db.gbanned
user_about_x = db.about_users

AZURE_API_KEY_URL_PREVIEW = "27b02a2c7d394388a719e0fdad6edb10"


@Cbot(pattern="^/(webss|sshot|screenshot) ?(.*)")
async def _(event):
    try:
        url = event.text.split(None, 1)[1]
    except IndexError:
        return await event.reply("Please provide the URL.")
    res = await event.reply("`Capturing Webpage...`")
    x = url.split(None)
    if len(x) == 2 and x[1] == "f":
        BASE = "https://webshot.deam.io/{url}?type={type}&quality={quality}&fullPage=true&height=540&width=960"
        final_url = BASE.format(url=url, type="jpeg", quality=100)
        try:
            await event.respond(file=final_url)
            return await res.delete()
        except BaseException as r:
            return await res.edit(str(r))
    BASE = "https://webshot.deam.io/{url}?type={type}&quality={quality}&height=1920&width=1080"
    final_url = BASE.format(url=url, type="jpeg", quality=100)
    g = get(final_url)
    f = open("webss.jpg", "wb")
    f.write(g.content)
    f.close()
    if not url.startswith("https://"):
        url = "https://" + url
    qurl = "https://api.labs.cognitive.microsoft.com/urlpreview/v7.0/search?q={url}"
    headers = {"Ocp-Apim-Subscription-Key": AZURE_API_KEY_URL_PREVIEW}
    r = get(qurl, headers=headers)
    url_data = ""
    if r.json()["_type"] == "ErrorResponse":
        print(url)
    else:
        try:
            url_data = r.json()["description"]
        except KeyError:
            url_data = ""
    try:
        await event.reply(url_data, file="webss.jpg", force_document=False)
        await res.delete()
    except Exception as e:
        await res.edit(str(e))


@Cbot(pattern="^/id ?(.*)")
async def aa(event):
    if not event.reply_to and not event.pattern_match.group(1):
        str(event.chat_id).replace("-100", "")
        return await event.reply(f"This chat's ID is: `{event.chat_id}`")
    user = None
    try:
        user, extra = await get_user(event)
        user_id = user.id
        name = user.first_name
        if not name:
            name = "User"
    except:
        pass
    skeletal = "User {}'s ID is `{}`."
    skeletal_fwd = """User {}'s ID is `{}`.
The forwarded user, {}, has an ID of `{}`"""
    skeletal_fwd_chat = """User {}'s ID is `{}`.
The forwarded channel, {}, has an id of `-100{}`."""
    if event.reply_to:
        msg = await event.get_reply_message()
        if msg.fwd_from:
            if msg.fwd_from.saved_from_peer:
                if isinstance(msg.fwd_from.saved_from_peer, types.PeerChannel):
                    try:
                        f_ch = await tbot.get_entity(
                            msg.fwd_from.saved_from_peer.channel_id
                        )
                    except:
                        return
                    skel_channel_post = "The posted channel, {}, has an id of `-100{}`."
                    return await event.reply(
                        skel_channel_post.format(f_ch.title, f_ch.id)
                    )
            elif msg.fwd_from.from_id:
                if isinstance(msg.fwd_from.from_id, types.PeerUser):
                    try:
                        f_user = await tbot.get_entity(msg.fwd_from.from_id)
                    except:
                        return
                    return await event.reply(
                        skeletal_fwd.format(name, user_id, f_user.first_name, f_user.id)
                    )
                elif isinstance(msg.fwd_from.from_id, types.PeerChannel):
                    try:
                        f_chat = await tbot.get_entity(msg.fwd_from.from_id)
                    except:
                        return
                    return await event.reply(
                        skeletal_fwd_chat.format(name, user_id, f_chat.title, f_chat.id)
                    )
    await event.reply(skeletal.format(name, user_id))


@Cbot(pattern="^/info ?(.*)")
async def _info(e):
    if not e.reply_to and not e.pattern_match.group(1):
        if e.sender_id:
            x_user = e.sender
    elif e.reply_to:
        reply_msg = await e.get_reply_message()
        if not reply_msg.sender_id:
            return
        x_user = reply_msg.sender
    elif e.pattern_match.group(1):
        x_obj = e.text.split(None, 1)[1]
        x_ov = x_obj.replace("-", "")
        if x_ov.isnumeric():
            x_obj = int(x_obj)
        try:
            x_user = await tbot.get_entity(x_obj)
        except (TypeError, ValueError) as x:
            return await e.reply(str(x))
    if isinstance(x_user, Channel):
        x_channel = await tbot(GetFullChannelRequest(x_user.username or x_user.id))
        out_str = f"<b>Channel Info:</b>"
        out_str += f"\n<b>Title:</b> {x_user.title}"
        if x_user.username:
            out_str += f"\n<b>Username:</b> @{x_user.username}"
        out_str += f"\n<b>Chat ID:</b> <code>{x_user.id}</code>"
        if x_user.verified:
            out_str += "\n<b>Verified:</b> True"
        if x_channel.full_chat.about:
            out_str += f"\n\n<b>Bio:</b> <code>{x_channel.full_chat.about}</code>"
        if len(x_channel.chats) == 2:
            out_str += f"\n<b>Linked Chat:</b> {x_channel.chats[1].title}"
            out_str += (
                f"\n<b>Linked Chat ID:</b> <code>-100{x_channel.chats[1].id}</code>"
            )
        if x_channel.full_chat.participants_count > 999:
            participants_count = human_format(x_channel.full_chat.participants_count)
        else:
            participants_count = x_channel.full_chat.participants_count
        out_str += f"\n\n<b>Participants:</b> <code>{participants_count}"
        if x_channel.full_chat.admins_count:
            out_str += f"\n<b>Admins:</b> <code>{x_channel.full_chat.admins_count}"
        file = x_channel.full_chat.chat_photo
        if isinstance(file, PhotoEmpty):
            file = None
        await e.reply(out_str, file=file, parse_mode="html")
    elif isinstance(x_user, User):
        x_full = await tbot(GetFullUserRequest(x_user.username or x_user.id))
        out_str = "<b>User Info:</b>"
        out_str += f"\n<b>First Name:</b> {x_full.user.first_name}"
        if x_full.user.last_name:
            out_str += f"\n<b>Last Name:</b> {x_full.user.last_name}"
        if x_full.user.username:
            out_str += f"\n<b>Username:</b> @{x_full.user.username}"
        out_str += f"\n<b>User ID:</b> <code>{x_full.user.id}</code>"
        out_str += (
            f"\n<b>PermaLink:</b> <a href='tg://user?id={x_full.user.id}'>link</a>"
        )
        if x_full.profile_photo and x_full.profile_photo.dc_id:
            out_str += f"\n<b>DC ID:</b> {x_full.profile_photo.dc_id}"
        if x_full.about:
            out_str += f"\n\n<b>Bio:</b> <code>{x_full.about}</code>"
        x_about = user_about_x.find_one({"user_id": x_full.user.id})
        if x_about:
            out_str += f"\n\n<b>What others Say:</b> <code>{x_about['about']}</code>"
        if x_full.user.id == OWNER_ID:
            out_str += f"\n\nThis is my Master, he have total power over me!"
        elif x_full.user.id in DEVS:
            out_str += f"\n\n<b>Status:</b> Commited(Dev)."
        elif x_full.user.id in SUDO_USERS:
            out_str += f"\n\n<b>Status:</b> Single(sudo)."
        if (
            not x_full.user.id in DEVS
            and not x_full.user.id in SUDO_USERS
            and not x_full.user.id == OWNER_ID
            and not x_full.user.id == BOT_ID
        ):
            if gbanned.find_one({"user": x_full.user.id}):
                x_gbanned = "Yes"
            else:
                x_gbanned = "No"
            if x_full.about:
                out_str += f"\n\n<b>Gbanned:</b> {x_gbanned}"
            else:
                out_str += f"\n<b>Gbanned:</b> {x_gbanned}"
            out_str += f"\n\n<b>BlackListed:</b> No"
        await e.reply(out_str, file=x_full.profile_photo, parse_mode="html")


@Cbot(pattern="^/setbio ?(.*)")
async def _(e):
    if not e.reply_to:
        return await e.reply("Reply to someone's message to set their bio!")
    reply_msg = await e.get_reply_message()
    if reply_msg.sender:
        if isinstance(reply_msg.sender, Channel):
            return
        user_id = reply_msg.sender_id
    else:
        return
    try:
        bio_words = e.text.split(None, 1)[1]
    except IndexError:
        return await e.reply("Give something as text to set their bio!")
    if user_id == e.sender_id:
        return await e.reply(
            "Ha, you can't set your own bio! You're at the mercy of others here..."
        )
    await e.reply(f"Updated {reply_msg.sender.first_name}'s Bio!")
    user_about_x.update_one(
        {"user_id": user_id}, {"$set": {"about": bio_words}}, upsert=True
    )


@Cbot(pattern="^/bin ?(.*)")
async def bin(event):
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        bin = msg.text
    elif event.pattern_match.group(1):
        bin = event.pattern_match.group(1)
    else:
        return await event.reply(
            "Enter a valid <b>Bin</b> to gather it's info.", parse_mode="html"
        )
    bin = bin.replace("x", "")
    url = "https://lookup.binlist.net/{}"
    response = get(url.format(bin))
    if not response:
        return await event.reply(
            f'<b>Invalid Bin❌</b>\n━━━━━━━━━━━━━\nChecked by <b><a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a></b>',
            parse_mode="html",
        )
    r = (response).json()
    country = r.get("country")
    bank = r.get("bank")
    out_str = f'**BIN/IIN:** `{bin}` {country.get("emoji")}'
    if r.get("scheme"):
        out_str += f'\n**Card Brand:** {(r.get("scheme")).upper()}'
    if r.get("type"):
        out_str += f'\n**Card Type:** {(r.get("type")).upper()}'
    if r.get("brand"):
        out_str += f'\n**Card Level:** {(r.get("brand")).upper()}'
    if r.get("prepaid"):
        out_str += f'\n**Prepaid:** {r.get("prepaid")}'
    if bank.get("name"):
        out_str += f'\n**Bank:** {bank.get("name")}'
    if country.get("name"):
        out_str += f'\n**Country:** {country.get("name")} - {country.get("alpha2")} - ${country.get("currency")}'
    if bank:
        if bank.get("url"):
            out_str += f'\n**Website:** `{bank.get("url")}`'
        if bank.get("phone"):
            out_str += f'\n**Contact:** {bank.get("phone")}'
    out_str += "\n**━━━━━━━━━━━━━**"
    out_str += (
        f"\nChecked by **[{event.sender.first_name}](tg://user?id={event.sender_id})**"
    )
    await event.reply(out_str, link_preview=False)


@Cbot(pattern="^/iban ?(.*)")
async def iban(event):
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        iban = msg.text
    elif event.pattern_match.group(1):
        iban = event.pattern_match.group(1)
    else:
        return await event.reply(
            "Enter a valid <b>Iban</b> to gather it's info.", parse_mode="html"
        )
    url = "https://api-2445580194301.production.gw.apicast.io/2.0/finance/iban/validate.php?value={}&language=en&app_id=a70d671c&app_key=0631709ede8501d226cad08369d60b22"
    r = (get(url.format(iban))).json()
    result = r.get("result")
    if not result == "valid":
        return await event.reply("Invalid iBAN.")
    out_str = "**IBAN:** `{iban}`"
    steps = r.get("steps")
    for x in steps:
        if x.get("validator_code") == "country_code_check":
            country = x.get("message")
            out_str += f"\n**Country:** {country}"
        elif x.get("validator_code") == "iban_length_check":
            length = x.get("message")
            out_str += f"\n**Length:** {length}"
        elif x.get("validator_code") == "bank_check":
            bank = x.get("message")
            out_str += f"\n**Bank:** {bank}"
    await event.reply(out_str)


@Cbot(pattern="^/define ?(.*)")
async def df(event):
    input = event.pattern_match.group(1)
    if not input:
        return await event.reply("Please give some input to search the dictionary!")
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/{}".format(input)
    r = get(url)
    try:
        r = r.json()[0].get("meanings")[0].get("definitions")[0].get("definition")
    except (TypeError, IndexError, KeyError):
        r = None
    if not r:
        return await event.reply("__No results found.__")
    await event.reply("**{}:**\n".format(input.capitalize()) + r)


@Cbot(pattern="^/ud ?(.*)")
async def ud(event):
    input = event.pattern_match.group(1)
    if not input:
        return await event.reply("Please give some input to search the dictionary!")
    results = get(f"http://api.urbandictionary.com/v0/define?term={input}").json()
    try:
        reply_text = f'**{input}:**\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
    except:
        reply_text = "No results found."
    await event.reply(reply_text)


@Cbot(pattern="^/ip ?(.*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await event.reply("Please provide an ipaddress to get its Details!")
    url = f"http://ip-api.com/json/{input_str}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
    response = get(url)
    info = response.json()
    valid = {info["status"]}
    if not "success" in valid:
        return await event.reply("Invalid IPAddress!")
    output = f"""
**IP Address:** `{info['query']}`
**ContinentCode:** {info['continentCode']}
**Country:** {info['country']}
**Country Code:** {info['countryCode']}
**Region:** {info['region']}
**Region Name:** {info['regionName']}
**City:** {info['city']}
**District:** {info['district']}
**Zip:** {info['zip']}
**Latitude:** `{info['lat']}`
**Longitude:** `{info['lon']}`
**Time Zone:** {info['timezone']}
**Offset:** {info['offset']}
**Currency:** {info['currency']}
**ISP:** {info['isp']}
**Org:** {info['org']}
**As:** {info['as']}
**Asname:** {info['asname']}
**Reverse:** {info['reverse']}
**User is on Mobile:** {info['mobile']}
**Proxy:** {info['proxy']}
**Hosting:** {info['hosting']}
"""
    await event.respond(output)


@Cbot(pattern="^/upload$")
async def up(event):
    if not event.reply_to:
        return
    msg = await event.get_reply_message()
    if not msg.media:
        return
    if msg.media.document:
        if int(msg.media.document.size) > 500000:
            return await event.reply("Failed, file size limit is 5MB.")
    res = await event.reply("Started download...")
    file_name = await tbot.download_media(msg)
    u = await res.edit(f"Success, Path: {file_name}")
    p = await u.edit("Now uploading to anonfiles...")
    cmd = "curl -F 'file=@" + file_name + "' https://api.anonfiles.com/upload"
    pr = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await pr.communicate()
    result = stdout
    result = result.decode("utf-8")
    result = result.split("{")
    result = result[4]
    result = result.split(",")
    result = result[0].replace('"full":', "")
    result = result.replace('"', "")
    os.remove(file_name)
    txt = f"<b>Uploaded to AnonFiles:</b>\n<code>{result}</code>"
    await p.edit(txt, parse_mode="html")


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


@Cbot(pattern="^/sysinfo ?(.*)")
async def CBP(e):
    if len(e.text.split(" ", 1)) == 2:
        pd = e.text.split(" ", 1)[1]
    else:
        pd = random.choice(
            [
                "ubuntu",
                "xubuntu",
                "lubuntu",
                "opensuse",
                "arch",
                "manjaro",
                "windows7",
                "windows10",
                "macos",
            ]
        )
    cmd = "neofetch --ascii_distro {}|sed 's/\x1B\\[[0-9;\\?]*[a-zA-Z]//g' >> neo.txt".format(
        pd
    )
    await bash(cmd)
    with open("neo.txt", "r") as neo:
        p = (neo.read()).replace("\n\n", "")
    options = carbon.CarbonOptions(
        p, language=random.choice(["python", "PHP", "JSON", "GO", "Ruby"])
    )
    cb = carbon.Carbon()
    im = await cb.generate(options)
    await im.save("neo")
    await e.reply(file="neo.png")
    os.remove("neo.png")
    os.remove("neo.txt")


@Cbot(pattern="^/carbon ?(.*)")
async def cb(event):
    if not event.reply_to and not event.pattern_match.group(1):
        return await event.reply(
            "Enter the text to make its image from `carbon.now.sh`."
        )
    elif event.reply_to:
        msg = await event.get_reply_message()
        if msg.media:
            if isinstance(msg.media, types.MessageMediaDocument):
                file = await tbot.download_media(msg)
                f = open(file)
                code = f.read()
                f.close()
                os.remove(file)
            else:
                if msg.text:
                    code = msg.raw_text
                else:
                    return
        else:
            code = msg.raw_text
    elif event.pattern_match.group(1):
        code = event.text.split(None, 1)[1]
    await event.reply("`Processing...`")
    options = carbon.CarbonOptions(
        code,
        language="python",
        background_color=random.choice(
            [
                (255, 0, 0, 1),
                (171, 184, 195, 1),
                (255, 255, 0, 1),
                (0, 0, 128, 1),
                (255, 255, 255, 1),
            ]
        ),
        font_family=random.choice(["Iosevka", "IBM Plex Mono", "hack", "Fira Code"]),
        adjust_width=True,
        theme=random.choice(["seti", "Night Owl", "One Dark"]),
    )
    cb = carbon.Carbon()
    try:
        img = await cb.generate(options)
    except:
        return
    await img.save("carbon")
    await event.respond(file="carbon.png")
    await res.delete()


@Cbot(pattern="^/(stoi|itos)$")
async def st(event):
    if not event.reply_to:
        return
    msg = await event.get_reply_message()
    if not msg.media:
        return
    f = await tbot.download_media(msg)
    action = event.pattern_match.group(1)
    if action == "itos":
        file = "sticker.webp"
        c = Image.open(f)
        c.save(file)
        await event.reply(file=file)
    elif action == "stoi":
        file = "image.png"
        c = Image.open(f)
        c.save(file)
        await event.reply(file=file)
    os.remove(f)
    os.remove(file)


def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a


couple_selection_message = """Couple of the day:
<a href="tg://user?id={}">{}</a> + <a href="tg://user?id={}">{}</a> = ❤️

New couple of the day may be chosen in {}"""


@Cbot(pattern="^/couple ?(.*)")
async def couple(event):
    today = str(dt()[0])
    tomorrow = str(dt_tom())
    if event.is_private:
        return await event.reply("This command only works in groups.")
    chat_id = event.chat_id
    is_selected = get_couple(chat_id, today)
    if not is_selected:
        users = []
        u_dict = {}
        async for user in tbot.iter_participants(chat_id):
            if not user.bot and user.first_name:
                users.append(user.id)
                u_dict[user.id] = user.first_name
        if len(users) < 2:
            return await event.reply("Not enough users")
        u1_id = random.choice(users)
        u2_id = random.choice(users)
        if u1_id == u2_id:
            u2_id = random.choice(users)
        u1_name = u_dict[u1_id]
        u2_name = u_dict[u2_id]
        couple = {
            "u1_id": u1_id,
            "u2_id": u2_id,
            "u1_name": u1_name,
            "u2_name": u2_name,
        }
        save_couple(chat_id, today, couple)
    elif is_selected:
        u1_id = int(is_selected["u1_id"])
        u2_id = int(is_selected["u2_id"])
        u1_name = is_selected["u1_name"]
        u2_name = is_selected["u2_name"]
    couple_final = couple_selection_message.format(
        u1_id, u1_name, u2_id, u2_name, tomorrow
    )
    cb_data = str(event.id) + "|" + "0" + "|" + "0"
    buttons = Button.inline("👍", data="upco_{}".format(cb_data)), Button.inline(
        "👎", data="downco_{}".format(cb_data)
    )
    await event.respond(couple_final, parse_mode="html", buttons=buttons)


@Cinline(pattern=r"upco(\_(.*))")
async def up(event):
    d = (((event.pattern_match.group(1)).decode()).split("_", 1)[1]).split("|")
    event_id = int(d[0])
    count1 = int(d[1])
    count2 = int(d[2])
    vote_up = voted_up(event_id, event.sender_id)
    vote_down = voted_down(event_id, event.sender_id)
    if vote_up:
        await event.answer("you took your reaction back.")
        rm_vote_up(event_id, event.sender_id)
        count1 -= 1
    elif vote_down:
        await event.answer("you 👍 this.")
        rm_vote_down(event_id, event.sender_id)
        count2 -= 1
        add_vote_up(event_id, event.sender_id)
        count1 += 1
    else:
        await event.answer("you 👍 this.")
        add_vote_up(event_id, event.sender_id)
        count1 += 1
    cb_data = str(event_id) + "|" + str(count1) + "|" + str(count2)
    C1 = count1
    C2 = count2
    if count1 == 0:
        C1 = ""
    if count2 == 0:
        C2 = ""
    edited_buttons = Button.inline(
        f"👍{C1}", data="upco_{}".format(cb_data)
    ), Button.inline(f"👎{C2}", data="downco_{}".format(cb_data))
    await event.edit(buttons=edited_buttons)


@Cinline(pattern=r"downco(\_(.*))")
async def up(event):
    d = (((event.pattern_match.group(1)).decode()).split("_", 1)[1]).split("|")
    event_id = int(d[0])
    count1 = int(d[1])
    count2 = int(d[2])
    vote_up = voted_up(event_id, event.sender_id)
    vote_down = voted_down(event_id, event.sender_id)
    if vote_down:
        await event.answer("you took your reaction back.")
        rm_vote_down(event_id, event.sender_id)
        count2 -= 1
    elif vote_up:
        await event.answer("you 👎 this.")
        rm_vote_up(event_id, event.sender_id)
        count1 -= 1
        add_vote_down(event_id, event.sender_id)
        count2 += 1
    else:
        await event.answer("you 👎 this.")
        add_vote_down(event_id, event.sender_id)
        count2 += 1
    cb_data = str(event_id) + "|" + str(count1) + "|" + str(count2)
    C1 = count1
    C2 = count2
    if count1 == 0:
        C1 = ""
    if count2 == 0:
        C2 = ""
    edited_buttons = Button.inline(
        f"👍{C1}", data="upco_{}".format(cb_data)
    ), Button.inline(f"👎{C2}", data="downco_{}".format(cb_data))
    await event.edit(buttons=edited_buttons)


@Cbot(pattern="^/tts ?(.*)")
async def tts(event):
    if not event.reply_to_msg_id and event.pattern_match.group(1):
        text = event.text.split(None, 1)[1]
        _total = text.split(None, 1)
        if len(_total) == 2:
            lang = (_total[0]).lower()
            text = _total[1]
        else:
            lang = "en"
            text = _total[0]
    elif event.reply_to_msg_id:
        text = (await event.get_reply_message()).text
        if event.pattern_match.group(1):
            lang = (event.pattern_match.group(1)).lower()
        else:
            lang = "en"
    else:
        return await event.reply(
            "`/tts <LanguageCode>` as reply to a message or `/tts <LanguageCode> <text>`"
        )
    try:
        tts = gTTS(text, tld="com", lang=lang)
        tts.save("stt.mp3")
    except BaseException as e:
        return await event.reply(str(e))
    aud_len = int((MP3("stt.mp3")).info.length)
    if aud_len == 0:
        aud_len = 1
    async with tbot.action(event.chat_id, "record-voice"):
        await event.respond(
            file="stt.mp3",
            attributes=[
                DocumentAttributeAudio(
                    duration=aud_len,
                    title=f"stt_{lang}",
                    performer="neko_chan",
                    waveform="320",
                )
            ],
        )
        os.remove("stt.mp3")


@Cbot(pattern="^/tr ?(.*)")
async def tr(event):
    w_out = False
    if not event.reply_to_msg_id and event.pattern_match.group(1):
        text = event.text.split(None, 1)[1]
        total = text.split(" ", 1)
        if len(total) == 2:
            lang = total[0]
            text = total[1]
        else:
            return await event.reply(
                "`/tr <LanguageCode>` as reply to a message or `/tr <LanguageCode> <text>`"
            )
    elif event.reply_to_msg_id:
        text = (await event.get_reply_message()).text
        if event.pattern_match.group(1):
            lang = event.pattern_match.group(1)
            if "-bare" in lang:
                lang = lang.replace("-bare", "")
                w_out = True
            elif lang == "-bare":
                lang = "en"
                w_out = True
        else:
            lang = "en"
    else:
        return await event.reply(
            "`/tr <LanguageCode>` as reply to a message or `/tr <LanguageCode> <text>`"
        )
    if "-bare" in text:
        text = text.replace("-bare", "")
        w_out = True
    trans = SyncTranslator()
    detect = trans.detect(text)
    q = trans(text, sourcelang=detect, targetlang=lang)
    if w_out:
        out_put = q.text
    else:
        out_put = "**Translated** from `{}` to `{}`:\n{}".format(detect, lang, q.text)
    await event.reply(out_put)


@Cbot(pattern="^/paste ?(.*)")
async def paste(e):
    paste_text = "n3ko"
    if not e.reply_to and not e.pattern_match.group(1):
        return await e.reply("What am I supposed to do with this?!")
    elif e.reply_to:
        if len(e.text.split(" ", 1)) == 2:
            mode = e.text.split(" ", 1)[1]
            if mode in ["h", "s", "p"]:
                sp_bin = mode
            else:
                sp_bin = "h"
        else:
            sp_bin = "h"
        reply_msg = await e.get_reply_message()
        if not reply_msg.media and reply_msg.text:
            paste_text = reply_msg.raw_text
        elif reply_msg.media:
            if not isinstance(reply_msg.media, MessageMediaDocument):
                return await e.reply("Reply to a text document to paste it!")
            else:
                file = await tbot.download_media(reply_msg)
                f = open(file, "rb")
                try:
                    paste_text = (f.read()).decode("utf-8")
                except UnicodeDecodeError as ude:
                    return await e.reply(str(ude))
                    os.remove("paste_file.txt")
                f.close()
                os.remove(file)
    elif e.pattern_match.group(1):
        paste_text = e.raw_text.split(None, 1)[1]
        sp_bin = "h"
    else:
        return
    paste_text = (paste_text.encode("utf-8")).decode("latin-1")
    haste_bin = "https://hastebin.com/documents"
    space_bin = "https://spaceb.in/api/v1/documents"
    pasty_bin = "https://pasty.lus.pm/api/v1/pastes"
    if sp_bin == "h":
        try:
            r = post(haste_bin, data=paste_text, timeout=2)
        except Exception:
            r = None
        if r and r.status_code == 200:
            try:
                key = r.json()["key"]
            except:
                sp_bin = "s"
            url = "https://hastebin.com/{}".format(key)
            bin = "HasteBin"
            bn = "Hasti"
        else:
            sp_bin = "s"
    if sp_bin == "s":
        r = post(space_bin, data={"content": paste_text, "extension": "py"})
        if r.ok and r.status_code == (201 or 200):
            try:
                r = r.json()
            except:
                sp_bin = "p"
            url = f"https://spaceb.in/{r['payload']['id']}"
            bin = "SpaceBin"
            bn = "Pasti"
        else:
            sp_bin = "p"
    if sp_bin == "p":
        r = post(
            pasty_bin,
            data=json.dumps({"content": paste_text}),
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
                "content-type": "application/json",
            },
        )
        if r.ok and r.status_code == 200:
            try:
                r = r.json()
            except:
                return
            url = f"https://pasty.lus.pm/{r['id']}.py"
            bin = "PastyBin"
            bn = "Pasti"
    await e.reply(
        f"{bn}fied to {bin}!\n**Pasted to {bin} !!**",
        buttons=Button.url("View Link", url),
    )


@Cbot(pattern="^/google ?(.*)")
async def google_search(e):
    try:
        query = e.text.split(None, 1)[1]
    except IndexError:
        return await e.reply("The query text has not been provided.")
    url = f"https://www.google.com/search?&q={query}&num=5"
    usr_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/61.0.3163.100 Safari/537.36"
    }
    r = get(url, headers=usr_agent)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("div", attrs={"class": "g"})
    final = f"Search Results for <b>{query}</b>:"
    if not results or len(results) == 0:
        return await e.reply("No results found!")
    for x in results:
        link = (x.find("a", href=True))["href"]
        name = x.find("h3")
        if link and name:
            if not name == "Images" and not name == "Description":
                final += f"\n- <a href='{link}'>{name}</a>"
    await e.reply(final, parse_mode="html", link_preview=False)


@Cbot(pattern="^/lyrics ?(.*)")
async def lyrics_get_(e):
    GENIUSES_API_KEY = (
        "gIgMyTXuwJoY9VCPNwKdb_RUOA_9mCMmRlbrrdODmNvcpslww_2RIbbWOB8YdBW9"
    )
    q = e.pattern_match.group(1)
    if not q:
        return await e.reply("Please provide the song name, to fetch its lyrics!")
    g_client = GeniusClient(GENIUSES_API_KEY)
    songs = g_client.search(q)
    if len(songs) == 0:
        return await e.reply("No result found for the given song name!")
    song = songs[0]
    name = song.title
    song.header_image_thumbnail_url
    lyrics = song.lyrics
    for x in ["Embed", "Share URL", "Copy"]:
        if x in lyrics:
            lyrics = lyrics.replace(x, "")
    pattern = re.compile("\n+")
    lyrics = pattern.sub("\n", lyrics)
    out_str = f"**{name}**\n__{lyrics}__"
    await e.reply(out_str)


kEys = [
    "mHfAkGq8Wi6dHHwt591nMAM7",
    "NSazBmGo6XfkS2LbTNZRiDdK",
    "Ad5bs76jsbssAAnEbx5PtBKe",
    "nDZ4WFe93Hn8Kjz3By8ALR7s",
]


@Cbot(pattern="^/rmbg ?(.*)")
async def remove_bg_photo_room__(e):
    if not e.reply_to:
        return await e.reply("Reply to any image to remove it's background.")
    r = await e.get_reply_message()
    if not r.photo and not r.sticker:
        return await e.reply("That's not a sticker/image to remove.bg")
    mxe = await e.reply("`Removing BG....`")
    f = await e.client.download_media(r)
    r = post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(f, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": random.choice(kEys)},
    )
    if r.ok:
        with open("rmbg.jpg", "wb") as w:
            w.write(r.content)
        await e.reply(file="rmbg.jpg", force_document=True)
        await mxe.delete()
    else:
        await e.reply(r.text)
    os.remove(f)


@Cbot(pattern="^/tx ?(.*)")
async def tx_test_(e):
    print("#")


@Cbot(pattern="^/(stat|stat)(@MissNeko_Bot|@missnekobot)?$")
async def ___stat_chat__(e):
    for x in ["+stats", "/stats", "!stats", "?stats"]:
        if e.text.startswith(x):
            return
    __stats_format = "**Total Messages in {}:** `{}`"
    await e.reply(__stats_format.format(e.chat.title, e.id))


@Cbot(pattern="^/read ?(.*)")
async def ocr_api_read__(e):
    OCR_API_KEY = "1f30d2c42b88957"
    if not e.is_reply:
        return await e.reply("Reply to an image/sticker to read it's text!")
    r = await e.get_reply_message()
    if not r.sticker and not r.photo:
        return await e.reply("That's not a valid sticker/image file!")
    f = await tbot.download_media(r)
    url = "https://api.ocr.space/parse/image"
    data = {"isOverlayRequired": False, "apikey": OCR_API_KEY}
    files = {"filename": open(f, "rb")}
    p = post(url, files=files, data=data)
    try:
        x = p.json().get("ParsedResults")[0].get("ParsedText")
    except (IndexError, KeyError, TypeError):
        return await e.reply("Failed to parse the image.")
    await e.reply("**Parsed Text:** " + "\n" + x)


@Cbot(pattern="^/img ?(.*)")
async def image_search_bing(e):
    q = e.text.split(None, 1)
    if not len(q) == 2:
        return
    q = q[1]
    search = bing_image_urls(q, limit=3)
    if len(search) == 0:
        return await e.reply("No search result found for your query!")
    try:
        await e.respond(file=search)
    except:
        pass


telegraph = Telegraph()
telegraph.create_account(short_name="neko")


@Cbot(pattern="^/telegraph(@MissNeko_Bot)? ?(.*)")
async def telegraph_upload___(e):
    if not e.reply_to and not len(e.text.split(" ", 1)) == 2:
        return await e.reply(
            "Reply to a message with correct arguments to get a permanent telegra.ph link."
        )
    if e.reply_to:
        r = await e.get_reply_message()
        if r.media and (r.photo or r.sticker):
            if isinstance(r.media, MessageMediaDocument):
                if r.media.document.size > 500000:
                    return await e.reply("Max file size reached, limit is 5MB.")
            xu = await e.reply("`Uploading....`")
            xp = await e.client.download_media(r)
            if xp.endswith("webp"):
                im = Image.open(xp)
                im.save(xp, "PNG")
            try:
                url = upload_file(xp)
            except Exception as ep:
                await xu.edit(str(ep))
            os.remove(xp)
            await xu.delete()
            await e.reply(
                f"Uploaded to **[Telegraph]**(https://telegra.ph{url[0]})!",
                buttons=Button.url(
                    xp or "Uploaded File", "https://telegra.ph{}".format(url[0])
                ),
            )
        elif r.document and "text" in r.media.document.mime_type:
            xu = await e.reply("`Uploading....`")
            xp = await e.client.download_media(r)
            fp = open(xp, "rb")
            fp = fp.readlines()
            try:
                fq = e.text.split(" ", 1)[1]
            except IndexError:
                fq = xp or "n3ko"
            fw = ""
            for x in fp:
                fw += x.decode() + "\n"
            fw = fw.replace("\n", "<br>")
            os.remove(xp)
            try:
                rp = telegraph.create_page(fq, html_content=fw)["path"]
            except Exception as re:
                return await xu.edit(str(re))
            await xu.edit(
                f"Pasted to **[Telegraph]**(https://telegra.ph/{rp})!",
                buttons=Button.url(
                    xp or "Pasted File", "https://telegra.ph/{}".format(rp)
                ),
            )
        elif r.text:
            try:
                fq = e.text.split(" ", 1)[1]
            except IndexError:
                fq = str(datetime.now())
            try:
                rp = telegraph.create_page(fq, html_content=r.text)["path"]
            except Exception as re:
                return await e.reply(str(re))
            await e.reply(
                f"Pasted to **[Telegraph]**(https://telegra.ph/{rp})!",
                buttons=Button.url("Pasted Text", "https://telegra.ph/{}".format(rp)),
            )
    elif len(e.text.split(" ", 1)) == 2:
        try:
            rp = telegraph.create_page(
                str(datetime.now()), html_content=e.text.split(" ", 1)[1]
            )["path"]
        except Exception as re:
            return await e.reply(str(re))
        await e.reply(
            f"Pasted to **[Telegraph]**(https://telegra.ph/{rp})!",
            buttons=Button.url("Pasted Text", "https://telegra.ph/{}".format(rp)),
        )


__name__ = "misc"
__help__ = """
Here is the help menu for **Misc** module:

- /webss `<url>`: generate screenshot of the website.
- /id `<user/chat/channel/forward>`: get the int id of the given entity.
- /info `<user/chat/channel>`: gather info about the given entity.
- /setbio `<text>`: set about bio of another user.
- /bin `<bin>`: gather info about the given bin.
- /iban `<iban>`: get info about the provided iban number.
- /define `<text>`: get definition of the given word from dictionary.
- /ud `<text>`: get definition from urban dictionary.
- /ip `<ip address>`: lookup the given ip address
- /stoi, /itos: Interconvert between Image and Sticker.
- /carbon `<text/reply>`: create beautiful image of the given text from carbon.now.sh .
- /couple: choose two random members of the chat as lovers.
- /tts `<LangCode> <text/reply>`: Text to speech provided by Google.
- /tr `<LangCode> <text/reply>`: translate between 200+ languages
Example: `/tr hi Hello`
- /paste `(h|s|p) <text/reply>`: Paste the text to Haste/Space/Pasty bins.
- /google `<query>`: perform a google search with the given query.
- /lyrics `<query>`: Gather the lyrics of the queried song from LyricsGenius.
- /rmbg `<reply>`: Remove bg of the image using `remove.bg` api.
- /read `<text/reply>`: Parse the text from the given image.
- /img `<query>`: Search for images from Google.
- /telegraph `<text/reply>`: Generate `telegra.ph` link with given media.
- /stat: Get Total message count of a chat.
"""
CMD_HELP.update({__name__: [__name__, __help__]})
