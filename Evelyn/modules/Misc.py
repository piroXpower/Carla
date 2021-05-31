import os
import random
from datetime import datetime

import requests
import stripe
from google_trans_new import google_translator
from PyDictionary import PyDictionary
from requests import get
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

from Evelyn import OWNER_ID, tbot, ubot
from Evelyn.events import Cbot
from Evelyn.modules.sql.misc_sql import ad_settings, add_ad

from . import ELITES, SUDO_USERS, can_change_info, get_user

BL = "sell buy vote ad rs btc usd netflix giveaway pornhub ss dm"


@Cbot(pattern="^/sshot ?(.*)")
async def _(event):
    BASE = "https://render-tron.appspot.com/screenshot/"
    url = event.pattern_match.group(1)
    if not url:
        return await event.reply("Please provide the URL.")
    path = "target.jpg"
    response = requests.get(BASE + url, stream=True)
    if not response.status_code == 200:
        return await event.reply("Invalid URL Provided.")
    else:
        X = await event.reply("Uploading the screenshot...")
        with open(path, "wb") as file:
            for chunk in response:
                file.write(chunk)
    await tbot.send_file(event.chat_id, path, reply_to=event.id, force_document=True)
    await X.delete()
    os.remove("target.jpg")


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
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        chat_id = str(event.chat_id).replace("-100", "")
        return await event.reply(
            f'<b><a href="t.me/c/{chat_id}">Chat ID</a>:</b> <code>{event.chat_id}</code>',
            parse_mode="html",
        )
    else:
        try:
            user, extra = await get_user(event)
        except TypeError:
            pass
    user_id = user.id
    name = user.first_name
    if not name:
        name = "ZeUzer"
    text = f'<b>User <a href="tg://user?id={user_id}">{name}</a>s ID:</b> <code>{user_id}</code>'
    await event.respond(text, parse_mode="html")


@Cbot(pattern="^/info ?(.*)")
async def _(event):
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        user = await tbot.get_entity(event.sender_id)
    else:
        try:
            user, extra = await get_user(event)
        except TypeError:
            pass
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
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
    if ups:
        text += f"\n\n<b>Bio:</b> <code>{ups.about}</code>"
        text += f"\n\n<b>BlackListed: No</b>"
        text += f"\n\n<b>Gbanned: No</b>"
        text += f"\n\n╘══「 <b>Groups count:</b> {ups.common_chats_count} 」"
    else:
        text += f"\n\n<b>BlackListed: No</b>"
        text += f"\n\n╘══「 <b>Gbanned:</b> No 」"
    await event.reply(text, parse_mode="html")


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
    await event.respond(text, parse_mode="htm")


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


@Cbot(pattern="^/ch ?(.*)")
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
        return await event.reply("Card number cannot be determined.")
    luv = event
    async with ubot.conversation("@carol5_bot") as conv:
        await conv.send_message(f"/ch {card}")
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


@Cbot(pattern="^/ck ?(.*)")
async def ck(event):
    card = event.pattern_match.group(1)
    if not card:
        return await event.reply("Enter the card.")
    try:
        card, month, year, cvc = card.split("|")
        card = card.strip()
        month = month.strip()
        year = year.strip()
        cvc = cvc.strip()
    except:
        return await event.reply("Invalid card format.")
    stripe.api_key = "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"
    k = stripe.Token.create(
        card={
            "number": card,
            "exp_month": month,
            "exp_year": year,
            "cvc": cvc,
        },
    )
    id = k["id"]
    try:
        fix = stripe.Charge.create(
            amount=100,
            currency="usd",
            source=id,
            description="KekK",
        )
    except stripe.error.CardError as e:
        return await event.reply(str(e))
    except stripe.error.InvalidRequestError as e:
        return await event.reply(str(e))
    await event.reply(str(fix))
