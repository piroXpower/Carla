import base64

from requests import post
from telethon.tl.types import Channel

colors = {
    "red",
    "green",
    "yellow",
    "orange",
    "violet",
    "indigo",
    "lightgreen",
    "tomato",
    "coral",
    "darkred",
    "gold",
    "lime",
    "darkgreen",
    "skyblue",
    "royalblue",
    "blue",
    "snow",
    "brown",
    "chocolate",
    "silver",
    "pink",
    "purple",
    "lime",
    "aqua",
    "white",
    "black",
    "gulabi",
    "gulambi",
}


@Cbot(pattern="^/q ?(.*)")
async def hq(event):
    if not event.reply_to:
        return await event.reply("Command must be sent as a reply to a message.")
    msg = await event.get_reply_message()
    color = "#1b1429"
    q_without_color = event.pattern_match.group(1)
    for c in colors:
        if c in event.pattern_match.group(1):
            q_without_color = (event.pattern_match.group(1)).replace(c, "")
            color = c
            if color in ["gulabi", "gulambi"]:
                color = "pink"
    reply_no = []
    if event.pattern_match.group(1):
        for x in event.pattern_match.group(1).split():
            if x.isdigit():
                reply_no.append(x)
                break
    if len(reply_no) == 0:
        reply_trigger = {}
        if msg.reply_to and "r" in q_without_color:
            r_msg = await msg.get_reply_message()
            reply_trigger = {
                "chatId": event.chat_id,
                "first_name": r_msg.sender.first_name,
                "last_name": r_msg.sender.last_name,
                "username": r_msg.sender.username,
                "text": r_msg.text,
                "name": r_msg.sender.first_name,
            }
        if not isinstance(msg.sender, Channel):
            _name = msg.sender.first_name
            if msg.fwd_from and msg.fwd_from.from_name:
                _name = msg.fwd_from.from_name
            data = {
                "type": "quote",
                "backgroundColor": color,
                "width": 512,
                "height": 768,
                "scale": 2,
                "messages": [
                    {
                        "entities": [],
                        "chatId": event.chat_id,
                        "avatar": True,
                        "from": {
                            "id": msg.sender_id,
                            "first_name": msg.sender.first_name,
                            "last_name": msg.sender.last_name,
                            "username": msg.sender.username,
                            "language_code": "en",
                            "title": "admin",
                            "photo": {},
                            "type": "private",
                            "name": _name,
                        },
                        "text": msg.raw_text,
                        "replyMessage": reply_trigger,
                    }
                ],
            }
            if msg.media:
                if msg.sticker:
                    data = {
                        "type": "quote",
                        "backgroundColor": color,
                        "width": 512,
                        "height": 768,
                        "scale": 2,
                        "messages": [
                            {
                                "media": [
                                    {
                                        "file_id": msg.file.id,
                                        "file_size": msg.file.size,
                                        "height": msg.file.height,
                                        "width": msg.file.width,
                                    }
                                ],
                                "mediaType": "sticker",
                                "entities": [],
                                "chatId": event.chat_id,
                                "avatar": True,
                                "from": {
                                    "id": msg.sender_id,
                                    "first_name": msg.sender.first_name,
                                    "last_name": msg.sender.last_name,
                                    "username": msg.sender.username,
                                    "language_code": "en",
                                    "title": "Admin",
                                    "photo": {},
                                    "type": "private",
                                    "name": msg.sender.first_name,
                                },
                                "text": msg.raw_text,
                                "replyMessage": reply_trigger,
                            }
                        ],
                    }
                elif msg.photo:
                    data = {
                        "type": "quote",
                        "backgroundColor": color,
                        "width": 512,
                        "height": 768,
                        "scale": 2,
                        "messages": [
                            {
                                "media": [
                                    {
                                        "file_id": msg.file.id,
                                        "file_size": msg.file.size,
                                        "height": msg.file.height,
                                        "width": msg.file.width,
                                    }
                                ],
                                "mediaType": "photo",
                                "entities": [],
                                "chatId": event.chat_id,
                                "avatar": True,
                                "from": {
                                    "id": msg.sender_id,
                                    "first_name": msg.sender.first_name,
                                    "last_name": msg.sender.last_name,
                                    "username": msg.sender.username,
                                    "language_code": "en",
                                    "title": "Admin",
                                    "photo": {},
                                    "type": "private",
                                    "name": msg.sender.first_name,
                                },
                                "text": msg.raw_text,
                                "replyMessage": reply_trigger,
                            }
                        ],
                    }
        else:
            data = {
                "type": "quote",
                "backgroundColor": color,
                "width": 512,
                "height": 768,
                "scale": 2,
                "messages": [
                    {
                        "entities": [],
                        "chatId": event.chat_id,
                        "avatar": True,
                        "from": {
                            "id": msg.sender.id,
                            "first_name": msg.sender.title,
                            "last_name": msg.sender.title,
                            "username": msg.sender.username,
                            "language_code": "en",
                            "title": "admin",
                            "photo": {},
                            "type": "private",
                            "name": msg.sender.title,
                        },
                        "text": msg.raw_text,
                        "replyMessage": reply_trigger,
                    }
                ],
            }
    else:
        return await event.respond(str(3))
    url = "https://bot.lyo.su/quote/generate"
    headers = {"Content-type": "application/json"}
    r = post(url, json=data, headers=headers)
    try:
        undecoded = r.json()["result"]["image"]
    except:
        return await event.reply(str(r))
    undecoded_bytes = bytes(undecoded, "utf-8")
    final_bytes = base64.b64decode((undecoded_bytes))
    if "p" in q_without_color:
        file = open("quotly.png", "wb")
        f_name = "quotly.png"
        f_doc = True
    else:
        file = open("quotly.webp", "wb")
        f_name = "quotly.webp"
        f_doc = False
    file.write(final_bytes)
    file.close()
    await event.respond(file=f_name, force_document=f_doc, reply_to=event.id)
