from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

import Evelyn.modules.sql.fsub_sql as sql
from Evelyn import BOT_ID, tbot
from Evelyn.events import Cbot

from . import is_admin, is_owner


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
        if not await is_admin(event.chat_id, event.sender_id):
            return await event.reply("You need to be an admin to do this.")
        if not await is_owner(event, event.sender_id):
            return
    channel = event.pattern_match.group(2)
    if not channel:
        chat_db = sql.fs_settings(event.chat_id)
        if not chat_db:
            await event.reply(
                "<b>❌ Force Subscribe is disabled in this chat.</b>", parse_mode="HTML"
            )
        else:
            await event.reply(
                "Forcesubscribe is currently <b>enabled</b>. Users are forced to join <b>@{chat_db.channel}</b> to speak here.",
                parse_mode="html",
            )
    elif channel in ["on", "yes", "y"]:
        await event.reply("❗Please specify the channel username.")
    elif channel in ["off", "no", "n"]:
        await event.reply("❗Forcesubscribe has been disabled for this chat.")
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
