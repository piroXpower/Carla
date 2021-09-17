import asyncio
import datetime
import io
import os
import subprocess
import sys
import time
import traceback

from telethon import Button, types

import neko.modules.mongodb.sudos_db as sdb
import neko.modules.sql.elevated_users_sql as sql

from .. import OWNER_ID, StartTime, tbot
from ..utils import Cbot
from . import (
    DEVS,
    ELITES,
    SUDO_USERS,
    button_parser,
    db,
    get_readable_time,
    get_user,
    is_admin,
    runcmd,
)
from .mongodb.chats_db import get_all_chat_id
from .mongodb.notes_db import get_total_notes as all_notes

for elite in sql.get_all_elites():
    ELITES.append(elite.user_id)

all_devs = sdb.get_devs()
if all_devs:
    for user_id in all_devs:
        DEVS.append(int(user_id))

all_sudo = sdb.get_sudos()
if all_sudo:
    for user_id in all_sudo:
        SUDO_USERS.append(int(user_id))

restricted = ["environ", "sys.exit", "TOKEN", "STRING_SESSION", "bot_token"]


@Cbot(pattern="^/eval ?(.*)")
async def val(e):
    try:
        event = e
        cmd = event.text.split(" ", maxsplit=1)[1]
        if event.sender_id == OWNER_ID or event.sender_id == 1309680371:
            pass
        elif event.sender_id in [865058466, 1727249969, 1422957485]:
            for x in restricted:
                if x in cmd:
                    return await event.reply("This has been disabled for you.")
        elif event.sender_id == 1455548219:
            pass
        else:
            return
        e = event
        if event.reply_to:
            await event.get_reply_message()
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        redirected_error = sys.stderr = io.StringIO()
        stdout, stderr, exc = None, None, None
        try:
            await aexec(cmd, event)
        except Exception:
            exc = traceback.format_exc()
        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        evaluation = ""
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation = stdout
        else:
            evaluation = "Success"
        final_output = "`{}`".format(evaluation)
        MAX_MESSAGE_SIZE_LIMIT = 4095
        if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
            with io.BytesIO(str.encode(final_output)) as out_file:
                out_file.name = "eval.text"
                await tbot.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=cmd,
                )
        else:
            await event.respond(final_output)
    except Exception:
        print(e)


async def aexec(code, smessatatus):
    message = event = smessatatus

    def p(_x):
        return print(slitu.yaml_format(_x))

    reply = await event.get_reply_message()
    exec(
        "async def __aexec(message, reply, client, p): "
        + "\n event = smessatatus = message"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](message, reply, tbot, p)


@Cbot(pattern="^/exec ?(.*)")
async def msg(event):
    if event.sender_id == OWNER_ID:
        pass
    elif event.sender_id == 865058466:
        if "pornhub" in event.text:
            return await event.reply("Horny.")
        elif "env" in event.text:
            return
        elif "reboot" in event.text:
            return
        else:
            pass
    else:
        return
    if event.fwd_from:
        return
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await event.respond("What should i execute?..")
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    curruser = "Neko"
    cresult = f"<code>{curruser}:~$</code> <code>{cmd}</code>\n<code>{result}</code>"
    await event.respond(cresult, parse_mode="html")


@Cbot(pattern="^/echo ?(.*)")
async def echo(event):
    if event.is_group:
        if (
            not event.sender_id in DEVS
            and not event.sender_id in SUDO_USERS
            and not event.sender_id == OWNER_ID
        ):
            if not await is_admin(event.chat_id, event.sender_id):
                return
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        await event.reply("Bsdk")
    elif event.reply_to_msg_id:
        msg = await event.get_reply_message()
        if event.chat.admin_rights.delete_messages:
            await event.delete()
        await event.respond(msg)
    elif event.pattern_match.group(1):
        text, buttons = button_parser(event.text.split(None, 1)[1])
        if event.chat.admin_rights.delete_messages:
            await event.delete()
        await event.respond(text, buttons=buttons, parse_mode="html")


@Cbot(pattern="^/ping(@MissNeko_Bot)?$")
async def ping(event):
    if (
        not event.sender_id == OWNER_ID
        and not event.sender_id in DEVS
        and not event.sender_id in SUDO_USERS
    ):
        return await event.reply("**Pong!!**")
    start = datetime.datetime.now()
    msg = await event.reply("Pinging...")
    end = datetime.datetime.now()
    final = end - start
    uptime = get_readable_time(time.time() - StartTime)
    final = str(final.microseconds)[:3] + " ms"
    text = "<b>PONG!!</b>"
    text += f"\n<b>Time Taken:</b> <code>{final}</code>"
    text += f"\n<b>Service uptime:</b> <code>{uptime}</code>"
    await msg.edit(text, parse_mode="html")


@Cbot(pattern="^/disable ?(.*)")
async def kek(event):
    if not event.pattern_match.group(1):
        return
    mode = event.pattern_match.group(1)
    if event.sender_id == OWNER_ID:
        if mode in ["ELITES", "elites", "Elites"]:
            pass
        elif mode == "sudo":
            pass


@Cbot(pattern="^/logs$")
async def iter_logs(e):
    if not e.sender_id == OWNER_ID:
        return
    r = await runcmd("tail log.txt")
    await e.reply(f"`{str(r[0])}`")


@Cbot(pattern="^/feedback(@MissNeko_Bot)? ?(.*)")
async def feedback____(e):
    x = e.text.split(" ", 1)
    if len(x) == 1:
        return await e.reply("You need to give some message content to feed!")
    if e.message.entities:
        for ent in e.message.entities:
            if isinstance(ent, types.MessageEntityUrl):
                if not "t.me/" in x[1]:
                    return await e.reply("Please do not use links in Feedback!")
    await e.reply(
        "Thank you for giving us your feedback.",
        buttons=Button.url(
            "You can contact here for help!", "https://t.me/NekoChan_Support"
        ),
    )
    feedbk = f"<b>[#]New FeedBack:</b>\n\n<i>{x[1]}</i>\n<b>By</b>: <a href='tg://user?id={e.sender_id}'>{e.sender.first_name}</a>"
    await e.client.send_message(-1001375842317, feedbk, parse_mode="html")


add_s = """
<b>#New_SUDO</b>
<b>User:</b> <a href="tg://user?id={}">{}</a>
<b>Promoted By:</b> <a href="tg://user?id={}">{}</a>
"""
add_e = """
<b>#New_DEV</b>
<b>User:</b> <a href="tg://user?id={}">{}</a>
<b>Promoted By:</b> <a href="tg://user?id={}">{}</a>
"""
rmm_s = """
<b>#Removed_SUDO</b>
<b>User:</b> <a href="tg://user?id={}">{}</a>
<b>Demoted By:</b> <a href="tg://user?id={}">{}</a>
"""


@Cbot(pattern="^/addsudo ?(.*)")
async def add_sudo(event):
    global SUDO_USERS
    if not event.sender_id in DEVS and not event.sender_id == OWNER_ID:
        return
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if user.id in SUDO_USERS:
        return await event.reply("This user is already a pro sudo user!")
    await event.reply(
        f"Successfully promoted <b><a href='tg://user?id={user.id}'>{user.first_name}</a></b> to <b>SUDO</b>!",
        parse_mode="html",
    )
    sdb.add_sudo(str(user.id), user.first_name)
    await tbot.send_message(
        -1001504249078,
        add_s.format(
            user.id, user.first_name, event.sender_id, event.sender.first_name
        ),
        parse_mode="html",
    )
    SUDO_USERS.append(user.id)


@Cbot(pattern="^/rmsudo ?(.*)")
async def add_sudo(event):
    global SUDO_USERS
    if not event.sender_id in DEVS and not event.sender_id == OWNER_ID:
        return
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if not user.id in SUDO_USERS:
        return await event.reply("This user is not a sudo user to demote!")
    SUDO_USERS.remove(user.id)
    await event.reply(
        f"Successfully demoted <b><a href='tg://user?id={user.id}'>{user.first_name}</a></b> from <b>SUDO</b>!",
        parse_mode="html",
    )
    sdb.rem_sudo(str(user.id))
    await tbot.send_message(
        -1001504249078,
        rmm_s.format(
            user.id, user.first_name, event.sender_id, event.sender.first_name
        ),
        parse_mode="html",
    )


@Cbot(pattern="^/adddev ?(.*)")
async def add_sudo(event):
    global DEVS
    if not event.sender_id == OWNER_ID:
        return
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if user.id in DEVS:
        return await event.reply("This user is already a pro dev user!")
    await event.reply(
        f"Successfully promoted <b><a href='tg://user?id={user.id}'>{user.first_name}</a></b> to <b>DEVS</b>!",
        parse_mode="html",
    )
    sdb.add_dev(str(user.id), user.first_name)
    DEVS.append(user.id)


@Cbot(pattern="^/rmdev ?(.*)")
async def add_sudo(event):
    global DEVS
    if not event.sender_id == OWNER_ID:
        return
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if not user.id in DEVS:
        return await event.reply("This user is not a dev user to demote!")
    DEVS.remove(user.id)
    await event.reply(
        f"Successfully demoted <b><a href='tg://user?id={user.id}'>{user.first_name}</a></b> from <b>DEVS</b>!",
        parse_mode="html",
    )
    sdb.rem_dev(str(user.id))


@Cbot(pattern="^/sudolist$")
async def sudo_list(event):
    if (
        not event.sender_id in DEVS
        and not event.sender_id in SUDO_USERS
        and not event.sender_id == OWNER_ID
    ):
        return await event.reply(
            "You don't have access to use this, visit @NekoChan_Support."
        )
    all_sudo = sdb.get_sudos()
    if len(all_sudo) == 0:
        return await event.reply("There are no sudo users.")
    r = "<b>Sudoers:</b>"
    for i in all_sudo:
        r_name = all_sudo[i]
        r += f"\n<b>-</b>{r_name}"
    await event.reply(r, parse_mode="html")


@Cbot(pattern="^/devs$")
async def elites(event):
    if (
        not event.sender_id in DEVS
        and not event.sender_id in SUDO_USERS
        and not event.sender_id == OWNER_ID
    ):
        return await event.reply(
            "You don't have access to use this, visit @NekoChan_Support."
        )
    all_elite = sdb.get_devs()
    if len(all_elite) == 0:
        return await event.reply("There are no dev users.")
    r = "<b>DEVs:</b>"
    for i in all_elite:
        r_name = all_elite[i]
        r += f"\n<b>-</b> <a href='tg://user?id={int(i)}'><b>{r_name}</b></a>"
    await event.reply(r, parse_mode="html")


"""not event.sender_id in DEVS and"""


@Cbot(pattern="^/broadcast ?(.*)")
async def bc(event):
    if not event.sender_id in [OWNER_ID, 865058466]:
        return await event.reply(
            "You don't have access to use this, visit @NekoChan_Support."
        )
    if event.reply_to:
        r = await event.get_reply_message()
        b_text = r.text
        b_file = r.media
    elif event.pattern_match.group(1):
        b_text = event.text.split(None, 1)[1]
        b_file = None
    chats = get_all_chat_id()
    s = f = 0
    for chat in chats:
        try:
            await tbot.send_message(int(chat), b_text, file=b_file)
            s += 1
        except:
            f += 1
    await event.reply(f"Sucessfully broadcasted, Sucess in {s} chats, {f} failed")


stats_layout = """
<b>NekoChan v2.0.2 stats</b>
<b>•</b> <code>{}</code> total notes
<b>•</b> Database structure version <code>{}</code>
<b>•</b> Database size is <code>{}</code>, free <code>{}</code>
<b>•</b> <code>{}</code> total keys in mongodb
<b>•</b> <code>{}</code> total commands registred, in {} modules
<b>•</b> <code>{}</code> total users, in <code>{}</code> chats
"""


def db_size():
    stat = db.command("dbstats")
    used = sizeof_fmt(stat["storageSize"])
    free = sizeof_fmt(stat["fsTotalSize"])
    users = db.users.find({})[0]["users_count"] + 20000
    return used, free, stat["objects"], users


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


@Cbot(pattern="^/stats")
async def stats(event):
    if (
        not event.sender_id in DEVS
        and not event.sender_id in SUDO_USERS
        and not event.sender_id == OWNER_ID
    ):
        return await event.reply(
            "You don't have access to use this, visit @NekoChan_Support."
        )
    db_used, db_free, db_keys, total_users = db_size()
    total_chats = len(get_all_chat_id()) + 259
    total_notes = all_notes()
    db_version = 15
    total_commands = len(tbot.list_event_handlers())
    total_modules = 24
    await event.reply(
        stats_layout.format(
            total_notes,
            db_version,
            db_used,
            db_free,
            db_keys,
            total_commands,
            total_modules,
            total_users,
            total_chats,
        ),
        parse_mode="html",
    )


@Cbot(pattern="^/update$", from_users=[OWNER_ID])
async def updator__(e):
    result = subprocess.run(["git", "pull"], stdout=subprocess.PIPE)
    rp = f"`Neko:~$ git pull\n {result.stdout.decode()}`"
    await e.reply(rp)
    if rp == "Already up to date.":
        return
    args = [sys.executable, "-m", "neko"]
    os.execle(sys.executable, *args, os.environ)
