import asyncio
import io
import sys
import traceback

from Evelyn import OWNER_ID, tbot
from Evelyn.events import Cbot

from . import ELITES, SUDO_USERS, button_parser, is_admin


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
        try:
            text, buttons = button_parser(event.pattern_match.group(1))
        except TypeError:
            text = button_parser(event.pattern_match.group(1))
            buttons = None
        if event.chat.admin_rights.delete_messages:
            await event.delete()
        await event.respond(text, buttons=buttons)
