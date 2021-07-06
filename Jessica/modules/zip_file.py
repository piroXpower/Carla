# from . import db
import os
import zipfile

from telethon import Button

from .. import tbot

zip_db = {}

from ..events import Cbot, Cinline


@Cbot(pattern="^/unzip")
async def e_unzip(event):
    if not event.reply_to:
        return
    zip_f = None
    if event.reply_to:
        zip_file = await event.get_reply_message()
        if not zip_file.media:
            return
        if not zip_file.file.name.endswith(".zip"):
            return await event.reply("That's not a zip file.")
        if zip_file.file.size > 500000:
            return await event.reply(
                "File size limit exceeds, The maximum file size allowed is 5MB."
            )
        x_text = """
Choose appropriate action 

🗃 = Normal files 
🔓 = Password protected files 
❌ = Cancel Process
"""
        x_buttons = [
            [
                Button.inline("Unzip🗃", data=f"unzip_{event.id}"),
                Button.inline("Password🔓", data=f"password_{event.id}"),
            ],
            [Button.inline("Cancel ❌", data="unzip_cancel")],
        ]
        await e.reply(x_text, buttons=x_buttons)
        zip_f = await tbot.download_media(zip_file)
        zip_db[event.id] = zip_f

    else:
        return


@Cinline(pattern="unzip_cancel")
async def unzip_cancel_cb(e):
    await e.delete()


@Cinline(pattern="unzip(\_(.*)")
async def unzip_e(e):
    e_id = int(((e.pattern_match.group(1)).decode()).split("_", 1)[1])
    try:
        zip_f = zip_db[e_id]
    except KeyError:
        await e.edit("File not found‼️")
    if zip_f:
        with zipfile.ZipFile(zip_f, "r") as zip_r:
            zip_r.extractall("./zip")
    unzip_dir = "zip/" + str(zip_f).replace(".zip", "")
    await x_r.edit(str(os.listdir(unzip_dir)))
