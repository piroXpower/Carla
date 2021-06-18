from telethon import Button, events
from telethon.errors import ChatAdminRequiredError
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

import Jessica.modules.sql.fsub_sql as sql
from Jessica import BOT_ID, OWNER_ID, tbot
from Jessica.events import Cbot

from . import ELITES, is_admin


async def participant_check(channel, user_id):
    try:
        result = await tbot(GetParticipantRequest(channel=channel, user_id=user_id))
        return True
    except UserNotParticipantError:
        return False


@Cbot(pattern="^/(fsub|Fsub|forcesubscribe|Forcesub|forcesub|Forcesubscribe) ?(.*)")
async def fsub(event):
    if event.is_private:
        return
    if event.is_group:
        perm = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not perm.is_admin:
            return await event.reply("You need to be an admin to do this.")
        if not perm.is_creator:
            return await event.reply(
                "❗ <b>Group Creator Required</b> \n<i>You have to be the group creator to do that.</i>",
                parse_mode="html",
            )
    channel = event.pattern_match.group(2)
    if not channel:
        chat_db = sql.fs_settings(event.chat_id)
        if not chat_db:
            await event.reply(
                "<b>❌ Force Subscribe is disabled in this chat.</b>", parse_mode="HTML"
            )
        else:
            await event.reply(
                f"Forcesubscribe is currently <b>enabled</b>. Users are forced to join <b>@{chat_db.channel}</b> to speak here.",
                parse_mode="html",
            )
    elif channel in ["on", "yes", "y"]:
        await event.reply("❗Please specify the channel username.")
    elif channel in ["off", "no", "n"]:
        await event.reply("**❌ Force Subscribe is Disabled Successfully.**")
        sql.disapprove(event.chat_id)
    else:
        try:
            channel_entity = await tbot.get_entity(channel)
        except:
            return await event.reply(
                "❗<b>Invalid channel Username provided.</b>", parse_mode="html"
            )
        channel = channel_entity.username
        try:
            channel_entity.broadcast
        except:
            return await event.reply("That's not a valid channel.")
        if not await participant_check(channel, BOT_ID):
            return await event.reply(
                f"❗**Not an Admin in the Channel**\nI am not an admin in the [channel](https://t.me/{channel}). Add me as a admin in order to enable ForceSubscribe.",
                link_preview=False,
            )
        sql.add_channel(event.chat_id, str(channel))
        await event.reply(f"✅ **Force Subscribe is Enabled** to @{channel}.")


@tbot.on(events.NewMessage(pattern=None))
async def nufsub(e):
    if not sql.fs_settings(e.chat_id):
        return
    if e.is_private:
        return
    if not e.from_id:
        return
    if (
        await is_admin(e.chat_id, e.sender_id)
        or e.sender_id in ELITES
        or e.sender_id == OWNER_ID
    ):
        return
    if not e.chat.admin_rights.ban_users:
        return
    channel = (sql.fs_settings(e.chat_id)).channel
    try:
        check = await participant_check(channel, e.sender_id)
    except ChatAdminRequiredError:
        return
    if not check:
        buttons = [Button.url("Join Channel", f"t.me/{channel}")], [
            Button.inline("Unmute Me", data="fs_{}".format(str(e.sender_id)))
        ]
        txt = f'<b><a href="tg://user?id={e.sender_id}">{e.sender.first_name}</a></b>, you have <b>not subscribed</b> to our <b><a href="t.me/{channel}">Channel</a></b> yet❗.Please <b><a href="t.me/{channel}">Join</a></b> and <b>press the button below</b> to unmute yourself.'
        await e.reply(txt, buttons=buttons, parse_mode="html", link_preview=False)
        await tbot.edit_permissions(e.chat_id, e.sender_id, send_messages=False)


@tbot.on(events.CallbackQuery(pattern=r"fs(\_(.*))"))
async def unmute_fsub(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    user_id = int(data.split("_", 1)[1])
    if not event.sender_id == user_id:
        return await event.answer("This is not meant for you.")
    channel = (sql.fs_settings(e.chat_id)).channel
    check = False
    try:
        check = await participant_check(channel, user_id)
    except ChatAdminRequiredError:
        return
    if not check:
        return await event.answer("Join the channel first")
    try:
        await tbot.edit_permissions(event.chat_id, user_id, send_messages=True)
    except ChatAdminRequiredError:
        pass
    await event.delete()