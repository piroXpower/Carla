# from telethon.tl.types import ChannelParticipantsAdmins

from neko.utils import Cbot

from . import can_change_info, get_user, is_admin
from .mongodb import reporting_db as db

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
    if event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    args = event.pattern_match.group(1)
    chat = event.chat_id
    if args:
        if args == "on" or args == "yes":
            await event.reply("Users will now be able to report messages.")
            db.set_chat_setting(chat, True)
        elif args == "off" or args == "no":
            await event.reply(
                "Users will no longer be able to report via @admin or /report."
            )
            db.set_chat_setting(chat, False)
        else:
            await event.reply("Your input was not recognised as one of: yes/no/on/off")
            return
    else:
        if db.chat_should_report(chat):
            await event.reply(Ron)
        else:
            await event.reply(Roff)


@Cbot(pattern="^/report ?(.*)")
async def _(event):
    if event.is_private:
        return  # add_reply
    if not db.chat_should_report(event.chat_id):
        return
    if await is_admin(event.chat_id, event.sender_id):
        return
    if not event.reply_to and not event.pattern_match.group(1):
        user = event.sender
    else:
        try:
            user, extra = await get_user(event)
        except TypeError:
            pass
    if await is_admin(event.chat_id, event.sender_id):
        return
    text = "Reported <a href='tg://user?id={}'>{}</a> to admins."
    await event.respond(
        text.format(user.id, user.first_name),
        parse_mode="html",
        reply_to=event.reply_to_msg_id or event.id,
    )


@Cbot(pattern="^@admin ?(.*)")
async def I(event):
    if event.is_private:
        return  # add_reply
    if not db.chat_should_report(event.chat_id):
        return
    if await is_admin(event.chat_id, event.sender_id):
        return
    user = None
    if not event.reply_to and not event.pattern_match.group(1):
        user = event.sender
    else:
        try:
            user, extra = await get_user(event)
        except TypeError:
            pass
    if await is_admin(event.chat_id, event.sender_id):
        return
    text = "Reported <a href='tg://user?id={}'>{}</a> to admins."
    await event.respond(
        text.format(user.id, user.first_name),
        parse_mode="html",
        reply_to=event.reply_to_msg_id or event.id,
    )


"""
async for users in tbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        text += f'<a href="tg://user?id={users.id}">&#8205;</a>'
"""
# will see later
