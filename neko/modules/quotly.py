from telethon.tl.types import Channel, User
from ..utils import Cbot
colors = [
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
]


@Cbot(pattern="^/q ?(.*)")
async def qoutly_api(e):
    if not e.reply_to:
        return await e.reply("Command must be sent as a reply to a message.")
    msg = await e.get_reply_message()
    color = "#1b1429"
    try:
        d = e.text.split(" ", 1)[1]
    except IndexError:
        d = ""
    for c in colors:
        if c in d:
            q_without_color = (d).replace(c, "")
            color = c
    num = [int(x) for x in d.split() if x.isdigit()]
    if not num:
        if "r" in q_without_color and msg.reply_to:
            reply = await msg.get_reply_message()
            if isinstance(reply.sender, Channel):
                reply_msg = {
                    "chatId": e.chat_id,
                    "first_name": reply.chat.title,
                    "last_name": "",
                    "username": reply.chat.username,
                    "text": reply.text,
                    "name": reply.chat.title,
                }
            elif reply.sender:
                name = reply.sender.first_name
                name = (
                    name + " " + reply.sender.last_name
                    if reply.sender.last_name
                    else name
                )
                reply_msg = {
                    "chatId": e.chat_id,
                    "first_name": reply.sender.first_name,
                    "last_name": "reply.sender.last_name",
                    "username": reply.sender.username,
                    "text": reply.text,
                    "name": name,
                }
            else:
                reply_msg = {}
        else:
            reply_msg = {}
        if isinstance(msg.sender, User):
            _name = msg.sender.first_name
            _name = (
                _name + " " + msg.sender.last_name if msg.sender.last_name else _name
            )
            if msg.fwd_from and msg.fwd_from.from_name:
                _name = msg.fwd_from.from_name
            _first = msg.sender.first_name
            _last = msg.sender.last_name
            _username = msg.sender.username
            _id = msg.sender_id
            _title = "Admin"
        elif isinstance(msg.sender, Channel):
            _name = msg.chat.title
            _first = _last = msg.chat.title
            _username = msg.chat.username
            _id = msg.chat_id
            _title = "Channel"
        else:
            _name = "Anonymous Admin"
            _first = _last = "Anon"
            _username = "GroupAnonymousBot"
            _id = 1087968824
            _title = "Gey"
        if msg.sticker:
            media = [
                {
                    "file_id": msg.file.id,
                    "file_size": msg.file.size,
                    "height": msg.file.height,
                    "width": msg.file.width,
                }
            ]
        elif msg.photo:
            media = [
                {
                    "file_id": msg.file.id,
                    "file_size": msg.file.size,
                    "height": msg.file.height,
                    "width": msg.file.width,
                }
            ]
        if msg.text:
            _text = msg.text
        else:
            _text = ""
        data = {
            "type": "quote",
            "backgroundColor": color,
            "width": 512,
            "height": 768,
            "scale": 2,
            "messages": [
                {
                    "entities": [],
                    "chatId": e.chat_id,
                    "avatar": True,
                    "from": {
                        "id": _id,
                        "first_name": _first,
                        "last_name": _last,
                        "username": _username,
                        "language_code": "en",
                        "title": _title,
                        "photo": {},
                        "type": "group",
                        "name": _name,
                    },
                    "text": _text,
                    "replyMessage": reply_msg,
                }
            ],
        }
    await e.reply(str(data))


"""
    if len(num) == 0:
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
     ids = [e.reply_to_msg_id, e.reply_to_msg_id - pd[0]]
     try:
      m = [x for x in e.client.iter_messages(e.chat_id, ids[0] -
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
"""
