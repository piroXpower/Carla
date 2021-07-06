# from . import db
import asyncio
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
                Button.inline("Password🔓", data=f"zpassword_{event.id}"),
            ],
            [Button.inline("Cancel ❌", data="unzip_cancel")],
        ]
        await event.reply(x_text, buttons=x_buttons)
        zip_db[event.id] = zip_file.file.name
        await tbot.download_media(zip_file)

    else:
        return


@Cinline(pattern="unzip_cancel")
async def unzip_cancel_cb(e):
    await e.delete()


@Cinline(pattern="zpassword(\_(.*))")
async def z_password(e):
    await e.answer("This feature is not available yet!", alert=True)


@Cinline(pattern="unzip(\_(.*))")
async def unzip_e(e):
    await e.edit("Processing...🚥")
    e_id = int(((e.pattern_match.group(1)).decode()).split("_", 1)[1])
    try:
        zip_f = zip_db[e_id]
    except KeyError:
        await e.edit("File not found‼️")
    if zip_f:
        try:
            with zipfile.ZipFile(zip_f, "r") as zip_r:
                zip_r.extractall("./zip")
        except zipfile.BadZipFile:
            await asyncio.sleep(4)
            try:
                with zipfile.ZipFile(zip_f, "r") as zip_r:
                    zip_r.extractall("./zip")
            except:
                await e.edit("File not found.")
    unzip_dir = "zip/" + str(zip_f).replace(".zip", "")
    x_files = os.listdir(unzip_dir)
    buttons = []
    x_buttons = []
    row_no = 0
    for q_file in x_files:
        row_no += 1
        q_btn = Button.inline(q_file, data=f"unzip_send_{q_file}")
        x_buttons.append(q_btn)
        if row_no == 2:
            buttons.append(x_buttons)
            x_buttons = []
            row_no = 0
    buttons.append([Button.inline("ALL", data="unzip_send_all"), Button.inline("Cancel", data="cancel_delete_file")])
    await e.edit("Choose the required Option...", buttons=buttons)
