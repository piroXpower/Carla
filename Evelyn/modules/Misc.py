import asyncio
import os
import random
import time
from datetime import datetime

import carbon
import requests
import stripe
from google_trans_new import google_translator
from PyDictionary import PyDictionary
from requests import get
from telethon import events, types
from telethon.errors import MediaEmptyError, WebpageCurlFailedError
from telethon.tl.functions.users import GetFullUserRequest

from Evelyn import OWNER_ID, tbot, ubot
from Evelyn.events import Cbot
from Evelyn.modules.sql.misc_sql import ad_settings, add_ad

from . import ELITES, SUDO_USERS, can_change_info, db, get_user

BL = "sell buy vote ad rs btc usd netflix giveaway pornhub ss dm"
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
    except (MediaEmptyError, WebpageCurlFailedError):
        await res.edit("__Invalid Url provided!__")


@Cbot(pattern="^/support ?(.*)")
async def _(event):
    if event.is_private:
        return
    args = event.pattern_match.group(1)
    if not args:
        return
    await tbot.send_message(
        -1001273171524,
        f"**(#)New Request Recieved**\n**From**: [{event.sender.first_name}](tg://user?id={event.sender_id})\n\n**Request:**\n`{args}`",
    )
    await event.reply("Sucessfully notified bot admins!")


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
    first_name = ""
    last_name = ""
    if user.first_name:
        first_name = ((user.first_name).replace("<", "&lt;")).replace(">", "&gt;")
    if user.last_name:
        last_name = ((user.last_name).replace("<", "&lt;")).replace(">", "&gt;")
    username = user.username
    text = "╒═══「<b>User info</b>:\n"
    if first_name:
        text += f"<b>First Name:</b> {first_name}\n"
    if last_name:
        text += f"<b>Last Name:</b> {last_name}\n"
    ups = None
    if username:
        text += f"<b>Username:</b> @{username}\n"
        ups = await ubot(GetFullUserRequest(user.username))
    text += f"<b>ID:</b> <code>{user_id}</code>\n"
    text += f'<b>User link:</b> <a href="tg://user?id={user_id}">{first_name}</a>'
    if user_id == OWNER_ID:
        text += "\n\n<i>This user is my Owner</i>"
    elif user_id in ELITES:
        text += "\n\n<i>This user is one of my Devs</i>"
    elif user_id in SUDO_USERS:
        text += "\n\n<i>This user is one of my Sudo Users</i>"
    gban_stat = gban_info(user_id)
    if ups:
        text += f"\n\n<b>Bio:</b> <code>{ups.about}</code>"
        text += f"\n\n<b>BlackListed: No</b>"
        text += f"\n\n<b>Gbanned: {gban_stat}</b>"
        text += f"\n\n╘══「 <b>Groups count:</b> {ups.common_chats_count} 」"
    else:
        text += f"\n\n<b>BlackListed: No</b>"
        text += f"\n\n╘══「 <b>Gbanned:</b> {gban_stat} 」"
    await event.reply(text, parse_mode="html")


def gban_info(user_id):
    if gbanned.find_one({"user": user_id}):
        return "Yes"
    return "No"


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
    if not response:
        return await event.reply(
            f'<b>Invalid Bin❌</b>\n━━━━━━━━━━━━━\nChecked by <b><a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a></b>',
            parse_mode="html",
        )
    k = response.json()
    try:
        emoji = k["country"]["emoji"]
    except KeyError:
        emoji = ""
    text = f"<b>BIN/IIN:</b> <code>{bin}</code> {emoji}"
    try:
        scheme = k["scheme"]
        if not scheme == None:
            text += f"\n<b>Card Brand:</b> <u>{scheme.upper()}</u>"
    except KeyError:
        pass
    try:
        type = k["type"]
        if not type == None:
            text += f"\n<b>Card Type:</b> {type.upper()}"
    except KeyError:
        pass
    try:
        brand = k["brand"]
        if not brand == None:
            text += f"\n<b>Card Level:</b> {brand.upper()}"
    except KeyError:
        pass
    try:
        prepaid = k["prepaid"]
        if not prepaid == None:
            text += f"\n<b>Prepaid:</b> {prepaid}"
    except KeyError:
        pass
    try:
        if not k["bank"] == None:
            name = k["bank"]["name"]
            text += f"\n<b>Bank:</b> {name}"
    except KeyError:
        pass
    try:
        if not k["country"] == None:
            name = k["country"]["name"]
            abr = k["country"]["alpha2"]
            currency = k["country"]["currency"]
            text += f"\n<b>Country:</b> {name} - {abr} - ${currency}"
    except KeyError:
        pass
    try:
        if not k["bank"] == None:
            url = k["bank"]["url"]
            text += f"\n<b>Website:</b> <code>{url}</code>"
    except KeyError:
        pass
    try:
        if not k["bank"] == None:
            phone = k["bank"]["phone"]
            text += f"\n<b>Contact:</b> <code>{phone}</code>"
    except KeyError:
        pass
    text += "\n━━━━━━━━━━━━━"
    text += f'\nChecked by <b><a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a></b>'
    await event.respond(
        text, parse_mode="htm", reply_to=event.reply_to_msg_id or event.id
    )


@Cbot(pattern="^/sk ?(.*)")
async def sk(event):
    if (
        event.text.startswith(".skick")
        or event.text.startswith("!skick")
        or event.text.startswith("/skick")
        or event.text.startswith("?skick")
    ):
        return
    api_key = event.pattern_match.group(1)
    if not api_key:
        return
    stripe.api_key = api_key
    timein = datetime.now()
    try:
        k = stripe.Source.create(
            type="ach_credit_transfer",
            currency="usd",
            owner={"email": "jenny.rosen@example.com"},
        )
        taken = datetime.now() - timein
        taken = str(round(taken.total_seconds(), 2)) + "s"
        valid = f"<b>Key:</b> <code>{api_key}</code>"
        valid += "\n<b>Response:</b> Valid Key✅"
        valid += f"\n<b>Time:</b> {taken}"
        valid += "\n━━━━━━━━━━━━━"
        valid += f'\nChecked by <b><a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a></b>'
        await event.respond(valid, parse_mode="html")
    except stripe.error.AuthenticationError as e:
        taken = datetime.now() - timein
        taken = str(round(taken.total_seconds(), 2)) + "s"
        valid = f"<b>Key:</b> <code>{api_key}</code>"
        valid += "\n<b>Response:</b> Invalid Key❌"
        valid += f"\n<b>Time:</b> {taken}"
        valid += "\n━━━━━━━━━━━━━"
        valid += f'\nChecked by <b><a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a></b>'
        await event.respond(valid, parse_mode="html")
    except stripe.error.InvalidRequestError as e:
        if "testmode" in str(e):
            taken = datetime.now() - timein
            taken = str(round(taken.total_seconds(), 2)) + "s"
            valid = f"<b>Key:</b> <code>{api_key}</code>"
            valid += "\n<b>Response:</b> TestMode Key❌"
            valid += f"\n<b>Time:</b> {taken}"
            valid += "\n━━━━━━━━━━━━━"
            valid += f'\nChecked by <b><a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a></b>'
            await event.respond(valid, parse_mode="html")
    except Exception as e:
        await event.respond(str(e))


@Cbot(pattern="^/cuhh ?(.*)")
async def ui(event):
    if (
        event.text.startswith(".chatbot")
        or event.text.startswith("/chatbot")
        or event.text.startswith("!chatbot")
        or event.text.startswith("?chatbot")
    ):
        return
    card = event.pattern_match.group(1)
    if not len(card) > 15 or not (card.replace("|", "")).isdigit():
        return await event.reply("**card number** cannot be determined.")
    luv = event
    async with ubot.conversation("@carol5_bot") as conv:
        await conv.send_message(f"ch {card}")
        response = await conv.get_response()
        if "Try again" in response.text:
            time = random.randint(20, 80)
            return await luv.reply(
                f"<b>Anti-Spam</b> Try again in <b>{time}s</b>", parse_mode="html"
            )
        peeps = await luv.reply("**Wait for result...**")

        @ubot.on(events.MessageEdited(from_users="carol5_bot"))
        async def hmm(event):
            arg = event.text.splitlines()
            if not len(arg) > 4:
                return await peeps.edit("Error")
            valid = "\n━━━━━━━━━━━━━"
            valid += f"\nChecked by **[{luv.sender.first_name}](tg://user?id={luv.sender_id})**"
            lu = len(arg)
            if lu == 8:
                await peeps.edit(
                    f"{arg[0]}\n{arg[1]}\n{arg[2]}\n{arg[3]}\n{arg[4]}\n{arg[5]}\n{arg[6]}"
                    + valid
                )
            elif lu == 7:
                await peeps.edit(
                    f"{arg[0]}\n{arg[1]}\n{arg[2]}\n{arg[3]}\n{arg[4]}\n{arg[5]}"
                    + valid
                )
            elif lu == 6:
                await peeps.edit(
                    f"{arg[0]}\n{arg[1]}\n{arg[2]}\n{arg[3]}\n{arg[4]}" + valid
                )
            elif lu == 5:
                await peeps.edit(f"{arg[0]}\n{arg[1]}\n{arg[2]}\n{arg[3]}" + valid)
            elif lu == 9:
                await peeps.edit(
                    f"{arg[0]}\n{arg[1]}\n{arg[2]}\n{arg[3]}\n{arg[4]}\n{arg[5]}\n{arg[6]}\n{arg[7]}"
                    + valid
                )


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
    if ban["valid"] == False:
        msg = ban["messages"]
        msg = str(msg).replace("[", "")
        msg = str(msg).replace("]", "")
        msg = str(msg).replace("'", "")
        valid = f"\n<b>IBan:</b> <code>{ibin}</code>"
        valid += "\n<b>Response:</b> Invalid IBan❌"
        valid += f"\n<b>Remarks:</b> <i>{msg}</i>"
        valid += "\n━━━━━━━━━━━━━"
        valid += f'\nChecked by <b><a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a></b>'
        return await event.respond(valid, parse_mode="html")
    elif ban["valid"] == True or ban["valid"] == "true":
        valid = f"\n<b>IBan:</b> <code>{ibin}</code>"
        valid += f"\n<b>Response:</b> Valid Iban✅"
        try:
            if ban["bankData"]:
                try:
                    code = ban["bankData"]["bankCode"]
                    valid += f"\n<b>Bank Code:</b> <code>{code}</code>"
                except KeyError:
                    pass
                try:
                    name = ban["bankData"]["name"]
                    valid += f"\n<b>Bank Name:</b> {name}"
                except KeyError:
                    pass
                try:
                    zip = ban["bankData"]["zip"]
                    valid += f"\n<b>Zip Code:</b> {zip}"
                except KeyError:
                    pass
                try:
                    city = ban["bankData"]["city"]
                    valid += f"\n<b>City:</b> {city}"
                except KeyError:
                    pass
                try:
                    bic = ban["bankData"]["bic"]
                    valid += f"\n<b>BIC:</b> <code>{bic}</code>"
                except KeyError:
                    pass
        except KeyError:
            pass
        valid += "\n━━━━━━━━━━━━━"
        valid += f'\nChecked by <b><a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a></b>'
        await event.respond(valid, parse_mode="htm")


@Cbot(pattern="^/antiads ?(.*)")
async def aa(event):
    pro = ["y", "yes", "on"]
    noob = ["n", "no", "off"]
    if event.is_private:
        return
    if not await can_change_info(event, event.sender_id):
        return
    args = event.pattern_match.group(1)
    if not args:
        mode = ad_settings(event.chat_id)
        await event.reply(f"Current Ad filter settings is : **__{mode}__**")
    elif args in pro:
        add_ad(event.chat_id, True)
        await event.reply("**Enabled** Ad filtering for this chat.")
    elif args in noob:
        add_ad(event.chat_id, False)
        await event.reply("**Disabled** Ad filtering for this chat.")
    else:
        await event.reply(
            f"`{args}` is not recognised as a valid input. Try one of y/yes/on/n/no/off."
        )


@Cbot(pattern="^/tr ?(.*)")
async def tr(event):
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
        else:
            lang = "en"
    else:
        return await event.reply(
            "`/tr <LanguageCode>` as reply to a message or `/tr <LanguageCode> <text>`"
        )
    translator = google_translator()
    try:
        translated = translator.translate(text, lang_tgt=lang)
        after_tr_text = translated
        detect_result = translator.detect(text)
        output_str = ("**Translated** from **__{}__** to **__{}__:**\n" "{}").format(
            detect_result[0], lang, after_tr_text
        )
        await event.reply(output_str)
    except Exception as exc:
        await event.reply(str(exc))


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


@Cbot(pattern="^/iplookup ?(.*)")
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


# balance soon


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


live_card = """
>. 𝐆𝐚𝐭𝐞𝐬/𝐀𝐮𝐭𝐡/𝐒𝐭𝐫𝐢𝐩𝐞

| —  𝐑𝐄𝐒𝐔𝐋𝐓
|- Card: <code>{}</code>
|- Status: <b>{}</b>
|- Code: <b>{}</b>
|- D-CODE: <b>{}</b>
|- Response: <b>{}</b>
| —  𝐁𝐈𝐍-𝐈𝐍𝐅𝐎
|- Bank/Type: <b>{}</b>
|- Country: <b>{}</b>
| —  𝐈𝐍𝐅𝐎𝐒
|- Checked By: <b>{}</b>
|- Time Taken:  <b>{}</b>
"""
decline_card = """
>. 𝐆𝐚𝐭𝐞𝐬/𝐀𝐮𝐭𝐡/𝐒𝐭𝐫𝐢𝐩𝐞

| —  𝐑𝐄𝐒𝐔𝐋𝐓
|- Card: <code>{}</code>
|- Status: <b>DECLINED ❌</b>
|- Code: <b>Invalid Card</b>
|- D-CODE: <b>Invalid Number</b>
|- Response: <b>your card number is incorrect</b>
| —  𝐁𝐈𝐍-𝐈𝐍𝐅𝐎
|- Bank/Type: 
|- Country: 
| —  𝐈𝐍𝐅𝐎𝐒
|- Checked By: <b>{}</b>
|- Time Taken:  <b>{}</b>
"""


@Cbot(pattern="^/auth ?(.*)")
async def ck(event):
    time_now = time.time()
    card = event.pattern_match.group(1)
    if not card:
        return
    final_ass = await event.reply("**Wait for result.**")
    async with ubot.conversation("@Possiblezbot") as conv:
        await conv.send_message(f"/chk {card}")
        res = await conv.get_response()
        lines = res.raw_text.splitlines()
        respn = lines[1].replace("Response: ", "")
        dict_1 = {}
        range_d = 0
        for line in res.raw_text.splitlines():
            if range_d == 3:
                break
            range_d += 1
            cmd, key = line.strip().split(":", 1)
            dict_1[cmd] = key.strip()
        range_d = 0
        dict_2 = {}
        for line in res.raw_text.splitlines():
            if range_d == 8:
                break
            range_d += 1
            if range_d in [7, 8]:
                cmd, key = line.strip().split(":", 1)
                dict_2[cmd] = key.strip()
        if dict_1["Response"] == "Approved":
            satst = "APPROVED ✅"
        else:
            satst = "DECLINED ❌"
        card_card = card.split("|", 1)[0]
        url = "https://lookup.binlist.net/{}"
        response = requests.request("GET", url.format(card_card))
        if not response:
            return await final_ass.edit(
                decline_card.format(card, event.sender.first_name, 69),
                parse_mode="html",
            )
        else:
            try:
                card_data = (
                    str(response.json()["brand"])
                    + " "
                    + str(response.json()["bank"]["name"])
                )
                card_country = (
                    str(response.json()["country"]["name"])
                    + " "
                    + str(response.json()["bank"]["emoji"])
                )
            except KeyError:
                card_data = dict_2[" Bank"]
                card_country = dict_2[" Country"]
        try:
            code, response = dict_1["Message"].split(":")
        except ValueError:
            code = dict_1["Message"]
            if satst == "DECLINED ❌":
                response = "your card was declined"
            else:
                response = ""
        final_time = time.time() - time_now
        await final_ass.edit(
            live_card.format(
                card,
                satst,
                code.strip(),
                code.strip(),
                response.strip(),
                card_data,
                card_country,
                event.sender.first_name,
                final_time,
            ),
            parse_mode="html",
        )


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
            r_text = "<b>Card number cannot be determined.</b>\nChecked By <b><a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a></b>"
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


slap_strings = (
    "{name_u} pokes {name_r} with a pen!",
    "{name_r} was struck by lightning.",
    "{name_u} best is what's for dinner!",
)


@Cbot(pattern="^/slap ?(.*)")
async def slap(event):
    random.choice(slap_strings)
