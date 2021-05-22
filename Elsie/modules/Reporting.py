from telethon.tl.types import ChannelParticipantsAdmins

from Elsie import OWNER_ID, tbot
from Elsie.events import Cbot
from Elsie.modules.sql import reporting_sql as sql

from . import ELITES, can_change_info, is_admin

Ron = """
Reports are currently enabled in this chat.
Users can use the /report command, or mention @admin, to tag all admins.

To change this setting, try this command again, with one of the following args: yes/no/on/off
"""
Roff = """
Reports are currently disabled in this chat.

To change this setting, try this command again, with one of the following args: yes/no/on/off
"""


@Cbot(pattern="^/reports ?(.*)")
async def _(event):
    if event.is_private:
        return  # connect
    if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
        k = await can_change_info(event, event.sender_id)
        if not k:
            return
    args = event.pattern_match.group(1)
    chat = event.chat_id
    if args:
        if args == "on" or args == "yes":
            await event.reply("Users will now be able to report messages.")
            sql.set_chat_setting(chat, True)
        elif args == "off" or args == "no":
            await event.reply(
                "Users will no longer be able to report via @admin or /report."
            )
            sql.set_chat_setting(chat, False)
        else:
            await event.reply("Your input was not recognised as one of: yes/no/on/off")
            return
    else:
        if sql.chat_should_report(chat):
            await event.reply(Ron)
        else:
            await event.reply(Roff)


@Cbot(pattern="^/report ?(.*)")
async def _(event):
    if event.is_private:
        return  # add_reply
    if not sql.chat_should_report(event.chat_id):
        return
    if await is_admin(event.chat_id, event.sender_id):
        return
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        id = msg.sender_id
        if await is_admin(event.chat_id, id):
            return
        name = msg.sender.first_name
    elif event.pattern_match.group(1):
        args = event.pattern_match.group(1)
        args = args.split()
        user = args[0]
        try:
            user = await tbot.get_entity(user)
        except:
            return await event.reply("Reported to admins.​")
        id = user.id
        if await is_admin(event.chat_id, user.id):
            return
        name = user.first_name
        if len(args) == 2:
            args[1]
    else:
        return await event.reply("Reported to admins.​")
    text = f'Reported <a href="tg://user?id={id}">{name}</a> to admins.'
    text = await gather_admins(event.chat_id, text)
    await event.reply(text, parse_mode="html")


async def gather_admins(chat_id, text):
    for users in await tbot.get_participants(chat_id, filter=ChannelParticipantsAdmins):
        text += f'<a href="tg://user?id={users.id}">&#8203;</a>'
    return text


@Cbot(pattern="^@admin ?(.*)")
async def I(event):
    if event.is_private:
        return  # add_reply
    if not sql.chat_should_report(event.chat_id):
        return
    if await is_admin(event.chat_id, event.sender_id):
        return
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        id = msg.sender_id
        if await is_admin(event.chat_id, id):
            return
        name = msg.sender.first_name
        event.pattern_match.group(1)
    elif event.pattern_match.group(1):
        args = event.pattern_match.group(1)
        args = args.split()
        user = args[0]
        try:
            user = await tbot.get_entity(user)
        except:
            return await event.reply("Reported to admins.​")
        id = user.id
        if await is_admin(event.chat_id, user.id):
            return
        name = user.first_name
        if len(args) == 2:
            args[1]
    else:
        return await event.reply("Reported to admins.​")
    text = f'Reported <a href="tg://user?id={id}">{name}</a> to admins.'
    await event.reply(text, parse_mode="html")
