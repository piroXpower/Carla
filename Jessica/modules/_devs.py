import asyncio
import datetime
import io
import sys
import time
import traceback

import Jessica.modules.sql.elevated_users_sql as sql
from Jessica import OWNER_ID, StartTime, tbot
from Jessica.events import Cbot
import Jessica.modules.mongodb.sudos_db as db
from . import ELITES, SUDO_USERS, button_parser, get_readable_time, get_user, is_admin, DEVS

for elite in sql.get_all_elites():
    ELITES.append(elite.user_id)

all_devs = db.get_devs()
for user_id in all_devs:
  DEVS.append(inf(user_id))

all_sudo = db.get_sudos()
for user_id in all_sudo:
  SUDO_USERS.append(int(user_id))

restricted = ["environ", "sys.exit", "TOKEN", "STRING_SESSION", "bot_token"]


@Cbot(pattern="^/eval ?(.*)")
async def val(event):
    try:
        cmd = event.text.split(" ", maxsplit=1)[1]
        if event.sender_id == OWNER_ID:
            pass
        elif event.sender_id == 1704673514:
            for x in restricted:
                if x in cmd:
                    return await event.reply("This has been disabled for you.")
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
    if not event.sender_id == OWNER_ID:
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
    curruser = "Jessica"
    cresult = f"`{curruser}:~$` `{cmd}`\n`{result}`"
    await event.respond(cresult)


@Cbot(pattern="^/echo ?(.*)")
async def echo(event):
    if event.is_group:
        if (
            not event.sender_id in ELITES
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


@Cbot(pattern="^/ping$")
async def ping(event):
    start = datetime.datetime.now()
    msg = await event.reply("Pinging...")
    end = datetime.datetime.now()
    final = end - start
    final = str(round(final.total_seconds(), 3))
    uptime = get_readable_time(time.time() - StartTime)
    final = (str(final)).replace("0.", "") + " ms"
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
async def logs(event):
    if not event.sender_id == OWNER_ID:
        return
    await event.respond("Kek")


@Cbot(pattern="^/addsudo ?(.*)")
async def add_sudo(event):
 if not event.sender_id in ELITES or not event.sender_id == OWNER_ID:
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
 await event.reply(f"Successfully promoted <b><a href='tg://user?id={user.id}'>{user.first_name}</a></b> to <b>SUDO</b>!",
        parse_mode="html",
    )
 db.add_sudo(str(user.id), user.first_name)
 SUDO_USERS.append(user.id)

@Cbot(pattern="^/rmsudo ?(.*)")
async def add_sudo(event):
 if not event.sender_id in ELITES or not event.sender_id == OWNER_ID:
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
 await event.reply(f"Successfully demoted <b><a href='tg://user?id={user.id}'>{user.first_name}</a></b> from <b>SUDO</b>!",
        parse_mode="html",
    )
 db.rm_sudo(str(user.id), user.first_name)
 SUDO_USERS.remove(user.id)
 


@Cbot(pattern="^/adddev ?(.*)")
async def add_sudo(event):
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
 await event.reply(f"Successfully promoted <b><a href='tg://user?id={user.id}'>{user.first_name}</a></b> to <b>ELITES</b>!",
        parse_mode="html",
    )
 db.add_dev(str(user.id), user.first_name)
 DEVS.append(user.id)


@Cbot(pattern="^/rmdev ?(.*)")
async def add_sudo(event):
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
 await event.reply(f"Successfully demoted <b><a href='tg://user?id={user.id}'>{user.first_name}</a></b> from <b>DEVS</b>!",
        parse_mode="html",
    )
 db.rm_dev(str(user.id), user.first_name)
 DEVS.remove(user.id)


@Cbot(pattern="^/sudolist$")
async def sudo_list(event):
    if (
        not event.sender_id in ELITES
        and not event.sender_id in SUDO_USERS
        and not event.sender_id == OWNER_ID
    ):
        return await event.reply(
            "You don't have access to use this, visit @NekoChan_Support."
        )
    all_sudo = db.get_sudos()
    r = "<b>SUDO Users:</b>"
    for i in all_sudo:
        r_name = all_sudo[i]["name"]
        r += f"\n<b>-</b> <a href='tg://user?id={int(i)}'><b>{r_name}</b></a>"
    await event.reply(r, parse_mode="html")


@Cbot(pattern="^/elites$")
async def elites(event):
    if (
        not event.sender_id in ELITES
        and not event.sender_id in SUDO_USERS
        and not event.sender_id == OWNER_ID
    ):
        return await event.reply(
            "You don't have access to use this, visit @NekoChan_Support."
        )
    all_elite = db.get_devs()
    r = "<b>ELITE Users:</b>"
    for i in all_elite:
        r_name = all_elite[i]["name"]
        r += f"\n<b>-</b> <a href='tg://user?id={int(i)}'><b>{r_name}</b></a>"
    await event.reply(r, parse_mode="html")
