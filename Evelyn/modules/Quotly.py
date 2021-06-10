import os
import textwrap
import urllib

from PIL import ImageFont
from telethon import functions, types

from Evelyn.events import Cbot

COLORS = [
    "#F07975",
    "#F49F69",
    "#F9C84A",
    "#8CC56E",
    "#6CC7DC",
    "#80C1FA",
    "#BCB3F9",
    "#E181AC",
]


def download_fonts():
    if not os.path.isdir(".tmp"):
        os.mkdir(".tmp", 0o755)
        urllib.request.urlretrieve(
            "https://github.com/erenmetesar/modules-repo/raw/master/Roboto-Regular.ttf",
            ".tmp/Roboto-Regular.ttf",
        )
        urllib.request.urlretrieve(
            "https://github.com/erenmetesar/modules-repo/raw/master/Quivira.otf",
            ".tmp/Quivira.otf",
        )
        urllib.request.urlretrieve(
            "https://github.com/erenmetesar/modules-repo/raw/master/Roboto-Medium.ttf",
            ".tmp/Roboto-Medium.ttf",
        )
        urllib.request.urlretrieve(
            "https://github.com/erenmetesar/modules-repo/raw/master/DroidSansMono.ttf",
            ".tmp/DroidSansMono.ttf",
        )
        urllib.request.urlretrieve(
            "https://github.com/erenmetesar/modules-repo/raw/master/Roboto-Italic.ttf",
            ".tmp/Roboto-Italic.ttf",
        )
    font = ImageFont.truetype(".tmp/Roboto-Medium.ttf", 43, encoding="utf-16")
    font2 = ImageFont.truetype(".tmp/Roboto-Regular.ttf", 33, encoding="utf-16")
    mono = ImageFont.truetype(".tmp/DroidSansMono.ttf", 30, encoding="utf-16")
    italic = ImageFont.truetype(".tmp/Roboto-Italic.ttf", 33, encoding="utf-16")
    fallback = ImageFont.truetype(".tmp/Quivira.otf", 43, encoding="utf-16")
    return font, font2, mono, italic, fallback


@Cbot(pattern="^/q ?(.*)")
async def quotly(event):
    if not event.reply_to:
        return
    reply = await event.get_reply_message()
    if reply.reply_to:
        await reply.get_reply_message()
    else:
        pass
    msg = reply.message
    user = (
        await event.client.get_entity(reply.forward.sender)
        if reply.fwd_from
        else reply.sender
    )
    font, font2, mono, italic, fallback = download_fonts()
    maxlength = 0
    width = 0
    text = []
    for line in msg.split("\n"):
        length = len(line)
        if length > 43:
            text += textwrap.wrap(line, 43)
            maxlength = 43
            if width < fallback.getsize(line[:43])[0]:
                if "MessageEntityCode" in str(reply.entities):
                    width = mono.getsize(line[:43])[0] + 30
                else:
                    width = fallback.getsize(line[:43])[0]
            next
        else:
            text.append(line + "\n")
            if width < fallback.getsize(line)[0]:
                if "MessageEntityCode" in str(reply.entities):
                    width = mono.getsize(line)[0] + 30
                else:
                    width = fallback.getsize(line)[0]
            if maxlength < length:
                maxlength = length
    title = ""
    try:
        details = await client(
            functions.channels.GetParticipantRequest(reply.chat_id, user.id)
        )
        if isinstance(details.participant, types.ChannelParticipantCreator):
            title = details.participant.rank if details.participant.rank else "Creator"
        elif isinstance(details.participant, types.ChannelParticipantAdmin):
            title = details.participant.rank if details.participant.rank else "Admin"
    except TypeError:
        pass
    font2.getsize(title)[0]
    await event.reply(str(maxlength) + "\nTitile: " + str(title))
