# from . import db
import os
import zipfile
from telethon import Button
from .. import tbot

zip_db = {}

from ..events import Cbot


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
        x_r = await event.reply("Started the file download!")
        zip_f = await tbot.download_media(zip_file)
    else:
        return
    if zip_f:
        with zipfile.ZipFile(zip_f, "r") as zip_r:
            zip_r.extractall("./zip")
    unzip_dir = str(zip_f).replace(".zip", "")
    await x_r.edit(str(os.listdir(unzip_dir)))


@Cbot(pattern="^/unzip_menu")
async def e_unzip_menu(e):
 x_text = """
Choose appropriate action 

🗃 = Normal files 
🔓 = Password protected files 
❌ = Cancel Process
"""
 x_buttons = [[Button.inline("Unzip🗃", data="unzip_f"), Button.inline("Password🔓", data="password")], [Button.inline("Cancel❌", data="unzip_cancel")]]
 await e.reply(x_text, buttons=x_buttons)
