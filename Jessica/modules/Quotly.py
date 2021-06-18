

COLORS = [
    "#F07975",
    "#F49F69",
    "#F9C84A",
    "#8CC56E",
    "#6CC7DC",
    "#80C1FA",
    "#BCB3F9",
    "#E181AC",
    "#1b1429",
]

import base64, random

from requests import post


@Cbot(pattern="^/q ?(.*)")
async def hq(event):
    if not event.reply_to:
        return
    msg = await event.get_reply_message()
    reply_trigger = {}
    if msg.reply_to and "r" in event.pattern_match.group(1):
        r_msg = await msg.get_reply_message()
        reply_trigger = {
            "chatId": event.chat_id,
            "first_name": r_msg.sender.first_name,
            "last_name": r_msg.sender.last_name,
            "username": r_msg.sender.username,
            "text": r_msg.raw_text,
            "name": r_msg.sender.first_name + r_msg.sender.last_name,
        }
    url = "https://bot.lyo.su/quote/generate"
    data = {
        "type": "quote",
        "backgroundColor": random.choice(COLORS),
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
                    "name": msg.sender.first_name,
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
                "backgroundColor": "#1b1429",
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
                "backgroundColor": "#1b1429",
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
    headers = {"Content-type": "application/json"}
    r = post(url, json=data, headers=headers)
    try:
     undecoded = r.json()["result"]["image"]
    except:
     return await event.reply(str(r.json()["result"]))
    undecoded_bytes = bytes(undecoded, "utf-8")
    final_bytes = base64.b64decode((undecoded_bytes))
    if "p" in event.pattern_match.group(1):
        file = open("quotly.png", "wb")
        f_name = "quotly.png"
        f_doc = True
    else:
        file = open("quotly.webp", "wb")
        f_name = "quotly.webp"
        f_doc = False
    file.write(final_bytes)
    file.close()
    await event.respond(file=f_name, force_document=f_doc)
