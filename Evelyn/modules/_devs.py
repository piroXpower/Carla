import asyncio
import datetime
import io
import sys
import time
import traceback

import Evelyn.modules.sql.elevated_users_sql as sql
from Evelyn import OWNER_ID, StartTime, tbot
from Evelyn.events import Cbot

from . import ELITES, SUDO_USERS, button_parser, get_readable_time, get_user, is_admin

sudos_sql = sql.get_all_sudos()
for sudo in sudos_sql:
    SUDO_USERS.append(sudo.user_id)

for elite in sql.get_all_elites():
    ELITES.append(elite.user_id)

@Cbot(pattern="^/eval ?(.*)")
async def val(event):
    try:
        cmd = event.text.split(" ", maxsplit=1)[1]
        if event.sender_id == OWNER_ID:
            pass
        else:
            return
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
    except Exception as e:
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
    curruser = "Evelyn"
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
    sudos = SUDO_USERS
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if user.id in sudos:
        return await event.reply("This user is already a sudo user.")
    await event.reply(f"Successfully promoted {user.first_name} to sudo!")
    sudos.append(user.id)
    sql.add_sudo(user.id, user.first_name)


@Cbot(pattern="^/rmsudo ?(.*)")
async def rmsudo(event):
    if not event.sender_id in ELITES or not event.sender_id == OWNER_ID:
        return
    sudos = SUDO_USERS
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if not user.id in sudos:
        return await event.reply("That is not a sudo user to demote!")
    await event.reply(f"Successfully demoted {user.first_name} from sudo!")
    sudos.remove(user.id)
    sql.remove_sudo(user.id)

@Cbot(pattern="^/addelite ?(.*)")
async def add_sudo(event):
    if event.sender_id in ELITES:
       return await event.reply("Only bot owner can add/remove elite users!")
    if not event.sender_id == OWNER_ID:
       return
    elite = ELITES
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if user.id in elite:
        return await event.reply("This user is already a **ELITE** user.")
    await event.reply(f"Successfully promoted {user.first_name} to **ELITE**!")
    elite.append(user.id)
    sql.add_elite(user.id, user.first_name)

@Cbot(pattern="^/rmelite ?(.*)")
async def add_sudo(event):
    if event.sender_id in ELITES:
       return await event.reply("Only bot owner can add/remove elite users!")
    if not event.sender_id == OWNER_ID:
       return
    elite = ELITES
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if not user.id in elite:
        return await event.reply("That is not an Elite user to demote!")
    await event.reply(f"Successfully demoted {user.first_name} from **ELITE**!")
    elite.remove(user.id)
    sql.remove_elite(user.id)
