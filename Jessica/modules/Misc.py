import asyncio
import os
import random
from datetime import datetime

import carbon
import requests
from gpytranslate import SyncTranslator
from gtts import gTTS
from mutagen.mp3 import MP3
from PyDictionary import PyDictionary
from requests import get, post
from telethon import Button, types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    DocumentAttributeAudio,
    MessageMediaDocument,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusRecently,
)

from Jessica import OWNER_ID, tbot, ubot
from Jessica.events import Cbot, Cinline
from Jessica.modules.mongodb.couples_db import (
    add_vote_down,
    add_vote_up,
    get_couple,
    rm_vote_down,
    rm_vote_up,
    save_couple,
    voted_down,
    voted_up,
)

from . import DEVS, SUDO_USERS, db, get_user

gbanned = db.gbanned


@Cbot(pattern="^/(webss|sshot|screenshot) ?(.*)")
async def _(event):
    url = event.pattern_match.group(2)
    if not url:
        return await event.reply("Please provide the URL.")
    BASE = "https://webshot.deam.io/{url}?type={type}&quality={quality}&fullPage=true&height=1080&width=1920"
    final_url = BASE.format(url=url, type="jpeg", quality=100)
    res = await event.reply("`Capturing Webpage...`")
    try:
        await event.reply(file=final_url)
        await res.delete()
    except BaseException as e:
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
async def _(event):
    user = None
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        user = await tbot.get_entity(event.sender_id)
    else:
        try:
            user, extra = await get_user(event)
        except TypeError:
            pass
    if not user:
        return
    user_id = user.id
    first_name = None
    last_name = None
    if user.first_name:
        first_name = ((user.first_name).replace("<", "&lt;")).replace(">", "&gt;")
    if user.last_name:
        last_name = ((user.last_name).replace("<", "&lt;")).replace(">", "&gt;")
    username = user.username
    text = "<b>╔═══「 Usᴇʀ Iɴғᴏ 」</b>\n"
    if first_name:
        text += f"<b>╠ Fɪʀsᴛ Nᴀᴍᴇ:</b> {first_name}\n"
    if last_name:
        text += f"<b>╠ Lᴀsᴛ Nᴀᴍᴇ:</b> {last_name}\n"
    ups = None
    file = None
    if username:
        text += f"<b>╠ UsᴇʀNᴀᴍᴇ:</b> @{username}\n"
        ups = await ubot(GetFullUserRequest(user.username))
    text += f"<b>╠ Usᴇʀ Iᴅ:</b> <code>{user_id}</code>\n"
    text += f'<b>╠ Pᴇʀᴍᴀ Lɪɴᴋ:</b> <a href="tg://user?id={user_id}">{first_name}</a>'
    if not user.bot:
        last_online = last_stat(user.status)
        text += f"\n<b>╠ Last Online:</b> <code>{last_online}</code>"
    puff = False
    if user_id in DEVS or user_id == OWNER_ID or user_id in SUDO_USERS:
        puff = True
        st = stats(user_id)
        if ups:
            text += f"\n<b>╠ Status:</b> <code>{st}</code>"
        else:
            text += f"\n<b>╚═══「 Status:</b> {st} <b>」</b>"
    if ups:
        if not puff:
            gban_stat = gban_info(user_id)
            text += f"\n<b>╠ GBᴀɴɴᴇᴅ:</b> {gban_stat}"
        text += f"\n<b>╚═══「 Gʀᴏᴜᴘ Cᴏᴜɴᴛ:</b> {ups.common_chats_count} <b>」</b>"
    elif not ups and not puff:
        gban_stat = gban_info(user_id)
        text += f"\n<b>╚═══「 GBᴀɴɴᴇᴅ:</b> {gban_stat}<b> 」</b>"
    try:
        file = (await tbot.get_profile_photos(username, limit=1))[0]
    except IndexError:
        file = None
    x_info = await event.reply(text, parse_mode="html", file=file)
    if ups.profile_photo:
        if ups.profile_photo.video_sizes:
            x_f = await tbot.download_media(ups.profile_photo)
            await x_info.edit(file=x_f)


def gban_info(user_id):
    if gbanned.find_one({"user": user_id}):
        return "Yᴇs"
    return "Nᴏ"


def last_stat(s):
    if isinstance(s, UserStatusRecently):
        return "Recently"
    elif isinstance(s, UserStatusLastMonth):
        return "Last Month"
    elif isinstance(s, UserStatusLastWeek):
        return "Last Week"
    else:
        return "Long Time Ago"


def stats(user_id):
    if user_id == OWNER_ID:
        return "Master"
    elif user_id in DEVS:
        return "Dev"
    elif user_id in SUDO_USERS:
        return "Sudo"


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
    response = requests.request("GET", url.format(bin))
    await event.reply(str(response.text))


@Cbot(pattern="^/iban ?(.*)")
async def iban(event):
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        ibin = msg.text
    elif event.pattern_match.group(1):
        ibin = event.pattern_match.group(1)
    else:
        return await event.reply(
            "Enter a valid <b>Iban</b> to gather it's info.", parse_mode="html"
        )
    iurl = f"https://openiban.com/validate/{ibin}?getBIC=true"
    response = get(iurl)
    ban = response.json()
    await event.reply(str(ban))


@Cbot(pattern="^/define ?(.*)")
async def df(event):
    input = event.pattern_match.group(1)
    if not input:
        return await event.reply("Please give some input to search the dictionary!")
    dictionary = PyDictionary()
    query = dictionary.meaning(str(input))
    query = str(query)
    query = query.replace("{", "")
    query = query.replace("}", "")
    query = query.replace("'", "")
    query = query.replace("[", "")
    query = query.replace("]", "")
    query = query.replace("(", "")
    query = query.replace(")", "")
    if str(query) == "None":
        return await event.reply("__No results found.__")
    await event.reply(str(query))


@Cbot(pattern="^/ud ?(.*)")
async def lilz(event):
    input = event.pattern_match.group(1)
    if not input:
        return await event.reply("Please give some input to search the dictionary!")
    results = get(f"http://api.urbandictionary.com/v0/define?term={input}").json()
    try:
        reply_text = f'**{input}:**\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
    except Exception:
        reply_text = "__No results found.__"
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
        if int(msg.media.document.size) > 1500000:
            return await event.reply("Failed, file size limit is 15MB.")
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


final_d_response = """
<b>{}</b>
▫️<u>Card:</u> <code>{}</code>
▫️<u>Result:</u> <b>{}</b>
▫️<u>D-code:</u> <b>{}</b>
▫️<u>BinData:</u> <b>{}</b>
▫️<u>Checked by:</u> <b><a href='tg://user?id={}'>{}</a></b></b>
"""


@Cbot(pattern="^/chk ?(.*)")
async def chk(event):
    if event.pattern_match.group(1):
        card = event.pattern_match.group(1)
    else:
        return
    async with ubot.conversation("@MarioChkBot") as chk:
        await chk.send_message(f"!chk {card}")
        response = await chk.get_response()
        if "Enter a valid format" in response.raw_text:
            r_text = f"<b>Card number cannot be determined.</b>\nChecked By <b><a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a></b>"
            return await event.reply(r_text, parse_mode="html")
        dict_1 = {}
        no = 0
        for x in response.raw_text.splitlines():
            no += 1
            if no in [2, 3, 4, 5]:
                x = x.replace("▫️", "")
                x = x.replace("__", "")
                x = x.replace("**", "")
                op, key = x.split(":", 1)
                dict_1[op] = key.strip()
        f_tt = final_d_response.format(
            response.raw_text.splitlines()[0],
            card,
            dict_1["Result"],
            dict_1["D-code"],
            dict_1["BinData"],
            event.sender_id,
            event.sender.first_name,
        )
        await event.reply(f_tt, parse_mode="html")


# balance soon
# afk
# good night
# 00:37
# gn
from PIL import Image


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
    color_code = random.choice(
        [
            (255, 0, 0, 1),
            (171, 184, 195, 1),
            (255, 255, 0, 1),
            (0, 0, 128, 1),
            (255, 255, 255, 1),
        ]
    )
    font = random.choice(["Iosevka", "IBM Plex Mono", "hack", "Fira Code"])
    options = carbon.CarbonOptions(
        code,
        language="python",
        background_color=color_code,
        font_family=font,
        adjust_width=True,
        theme="seti",
    )
    cb = carbon.Carbon()
    img = await cb.generate(options)
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


couple_selection_message = """Couple of the day: <b><a href="tg://user?id={}">{}</a> + <a href="tg://user?id={}">{}</a></b> = ❤️

<i>New couple of the day may be chosen at 12AM {}</i>"""


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
            lang = _total[0]
            text = _total[1]
        else:
            lang = "en"
            text = _total[0]
    elif event.reply_to_msg_id:
        text = (await event.get_reply_message()).text
        if event.pattern_match.group(1):
            lang = event.pattern_match.group(1)
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
        await event.reply(
            file="stt.mp3",
            attributes=[
                DocumentAttributeAudio(
                    duration=aud_len,
                    title="stt",
                    performer="Neko-Chan",
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
async def paste_api(e):
    paste_text = "None"
    if not e.reply_to and not e.pattern_match.group(1):
        return await e.reply("What am I supposed to do with this?!")
    elif e.reply_to:
        reply_msg = await e.get_reply_message()
        if not reply_msg.media and reply_msg.text:
            paste_text = reply_msg.raw_text
        elif reply_msg.media:
            if not isinstance(reply_msg.media, MessageMediaDocument):
                return await e.reply("Reply to a text document to paste it!")
            else:
                await tbot.download_media(reply_msg, "paste_file.txt")
                f = open("paste_file.txt", "rb")
                try:
                    paste_text = (f.read()).decode("utf-8")
                except UnicodeDecodeError as ude:
                    return await e.reply(str(ude))
                    os.remove("paste_file.txt")
                f.close()
                os.remove("paste_file.txt")
    elif e.pattern_match.group(1):
        paste_text = e.raw_text.split(None, 1)[1]
    else:
        return
    paste_text = (paste_text.encode("utf-8")).decode("latin-1")
    api_url = "https://hastebin.com/documents"
    response = post(api_url, data=paste_text)
    r_key = response.json()["key"]
    await e.reply("Pasted to [Haste-Bin](https://hastebin.com/{})!".format(r_key))
