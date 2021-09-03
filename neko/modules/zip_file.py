import asyncio
import datetime
import os
import zipfile

from telethon import Button

from .. import tbot
from . import db

zip_db = {}
zip_files_db = {}
zip_info_db = {}
zip_back_files_db = {}
x_db = db.zip_users
from math import ceil

from ..utils import Cbot, Cinline


@Cbot(pattern="^/unzip")
async def e_unzip(event):
    x_u = x_db.find_one({"user_id": event.sender_id})
    if x_u:
        x_time_wait = (datetime.datetime.now() - x_u["date_added"]).total_seconds()
        x_time_wait_format = 60 - int(x_time_wait)
        if x_time_wait < 60:
            return await event.reply(
                "You have to wait `{}` seconds before using this command again.".format(
                    x_time_wait_format
                )
            )
        else:
            pass
    x_db.update_one(
        {"user_id": event.sender_id},
        {"$set": {"date_added": datetime.datetime.now()}},
        upsert=True,
    )
    if not event.reply_to:
        return
    if event.reply_to:
        zip_file = await event.get_reply_message()
        if not zip_file.media:
            return
        if not zip_file.file.name.endswith(".zip"):
            return await event.reply("That's not a zip file.")
        if zip_file.file.size > 3464400:
            return await event.reply(
                "File size limit exceeds, The maximum file size allowed is 3.5MB."
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
                zip_r.extractall("./zip/" + str(zip_f).replace(".zip", ""))
        except zipfile.BadZipFile:
            await asyncio.sleep(4)
            try:
                with zipfile.ZipFile(zip_f, "r") as zip_r:
                    zip_r.extractall("./zip/" + str(zip_f).replace(".zip", ""))
            except:
                await e.edit("File not found.")
    if os.path.isdir(
        "zip/" + str(zip_f).replace(".zip", "") + "/" + str(zip_f).replace(".zip", "")
    ):
        unzip_dir = (
            "zip/"
            + str(zip_f).replace(".zip", "")
            + "/"
            + str(zip_f).replace(".zip", "")
        )
    else:
        unzip_dir = "zip/" + str(zip_f).replace(".zip", "")
    x_files = os.listdir(unzip_dir)
    zip_info_db[zip_f] = x_files
    for q_file in x_files:
        zip_files_db[q_file] = unzip_dir + "/"
    x_bt = paginate_zip(0, x_files, zip_f)
    await e.edit("Choose the required Option...", buttons=x_bt)


@Cinline(pattern="unz_send(\_(.*))")
async def unz_send(e):
    x_file_name = ((e.pattern_match.group(1)).decode()).split("_", 1)[1]
    if x_file_name == "all":
        return await e.answer("Shoon!", alert=True)
    try:
        x_path = zip_files_db[x_file_name]
    except KeyError:
        return await e.answer("404, File not found.", alert=True)
    if os.path.isdir(x_path + x_file_name):
        try:
            zip_back_files_db[x_file_name] = os.listdir(x_path)
            x_plus_files = os.listdir(x_path + x_file_name)
            for q_file in x_plus_files:
                zip_files_db[q_file] = x_path + x_file_name + "/"
            zip_info_db[x_file_name] = x_plus_files
            buttons = paginate_zip(0, x_plus_files, x_file_name, True)
            return await e.edit(buttons=buttons)
        except KeyError:
            return
    await e.delete()
    try:
        await e.respond(file=x_path + x_file_name)
    except ValueError:
        await e.respond("404, File not found! Or Zip file is Corrupt.")


@Cinline(pattern="zip_next(\_(.*))")
async def zip_next(e):
    page_data = (((e.pattern_match.group(1)).decode()).split("_", 1)[1]).split("|", 1)
    page_no = int(page_data[0])
    x_name = page_data[1]
    try:
        zip_files = zip_info_db[x_name]
    except KeyError:
        return
    buttons = paginate_zip(page_no + 1, zip_files, x_name)
    await e.edit(buttons=buttons)


@Cinline(pattern="zip_prev(\_(.*))")
async def zip_prev(e):
    page_data = (((e.pattern_match.group(1)).decode()).split("_", 1)[1]).split("|", 1)
    page_no = int(page_data[0])
    x_name = page_data[1]
    try:
        zip_files = zip_info_db[x_name]
    except KeyError:
        return
    buttons = paginate_zip(page_no - 1, zip_files, x_name)
    await e.edit(buttons=buttons)


def paginate_zip(page, zip_files, x_name, back_btn=False):
    plugins = sorted(zip_files)
    x_buttons = [
        Button.inline("{}".format(x), data="unz_send_{}".format(x)) for x in plugins
    ]
    pairs = list(zip(x_buttons[::2], x_buttons[1::2]))
    if len(x_buttons) % 2 == 1:
        pairs.append((x_buttons[-1],))
    max_num_pages = ceil(len(pairs) / 4)
    if max_num_pages == 0:
        max_num_pages = 1
    modulo_page = page % max_num_pages
    cb_data = str(modulo_page) + "|" + str(x_name)
    if len(pairs) <= 4:
        x_a = (Button.inline("ALL", data="unz_send_all"),)
        x_b = (
            Button.inline("Cancel", data="zip_exit"),
            Button.inline("Back", data="zip_back_{}".format(cb_data)),
        )
        pairs.append(x_a)
        pairs.append(x_b)
    if len(pairs) > 4:
        pairs = (
            pairs[modulo_page * 4 : 4 * (modulo_page + 1)]
            + [
                (
                    Button.inline("<<", data="zip_prev_{}".format(cb_data)),
                    Button.inline("ALL", data="unz_send_all"),
                    Button.inline(">>", data="zip_next_{}".format(cb_data)),
                )
            ]
            + [
                (
                    Button.inline("Cancel", data="zip_exit"),
                    Button.inline("Back", data="zip_back_{}".format(cb_data)),
                )
            ]
        )
    return pairs


@Cinline(pattern="zip_back(\_(.*))")
async def zip_back(e):
    x_name = (((e.pattern_match.group(1)).decode()).split("_", 1)[1]).split("|", 1)[1]
    # print(x_name)
    try:
        zip_files = zip_back_files_db[x_name]
    except KeyError:
        return await e.answer(x_name, alert=True)
    buttons = paginate_zip(0, zip_files, str(x_name))
    await e.edit(buttons=buttons)


# fix
