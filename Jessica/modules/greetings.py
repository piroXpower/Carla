from telethon import types, events
from Jessica import tbot
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantBanned,
    UpdateChannelParticipant,
)

import Jessica.modules.mongodb.welcome_db as db

from . import button_parser, can_change_info, get_reply_msg_btns_text

buttons = None


def get_fileids(r_msg):
    if isinstance(r_msg.media, types.MessageMediaDocument):
        file_id = r_msg.media.document.id
        access_hash = r_msg.media.document.access_hash
        file_reference = r_msg.media.document.file_reference
        type = "doc"
    elif isinstance(r_msg.media, types.MessageMediaPhoto):
        file_id = r_msg.file.id
        access_hash = None
        file_reference = None
        type = "photo"
    else:
        return None, None, None, None
    return file_id, access_hash, file_reference, type


async def welcome_fill(chat_id, user_id):
    chat = await tbot.get_entity(chat_id)
    user = await thot.get_entity(user_id)
    user.bot
    first_name = user.first_name
    last_name = user.last_name
    mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
    full_name = first_name
    if last_name:
        full_name = first_name + last_name
    user.username
    title = chat.title
    return first_name, last_name, mention, full_name, chat_id, id, title


def idto_file(id, hash, ref, type):
    if not id:
        return None
    elif type == "doc":
        return types.InputDocument(id=id, access_hash=hash, file_reference=ref)
    elif type == "photo":
        return id
    else:
        return None


@Cbot(pattern="^/setwelcome ?(.*)")
async def set_welxome(event):
    if event.is_private:
        return await event.reply("nope")
    if not event.from_id:
        return await a_welcome(event, "setwelcome")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    if not event.reply_to and not event.pattern_match.group(1):
        return await event.reply("You need to give the welcome message some content!")
    elif event.reply_to:
        r_msg = await event.get_reply_message()
        id, hash, ref, type = get_fileids(r_msg)
        if r_msg.text:
            r_text = r_msg.text
        else:
            r_text = None
        if r_msg.reply_markup:
            r_text = r_text + get_reply_msg_btns_text(r_msg)
    elif event.pattern_match.group(1):
        id = hash = ref = type = None
        r_text = event.text.split(None, 1)[1]
    await event.reply("The new welcome message has been saved!")
    db.set_welcome(event.chat_id, r_text, id, hash, ref, type)


@Cbot(pattern="^/resetwelcome")
async def rw(event):
    if event.is_private:
        return await event.reply("This command is made to used in group chats!")
    if not event.from_id:
        return await a_welcome(event, "resetwelcome")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    await event.reply("The welcome message has been reset to default!")
    db.reset_welcome(event.chat_id)


w_str = """
I am currently welcoming users: {}
I am currently deleting old welcomes: 
I am currently deleting service messages: 
CAPTCHAs are .
Welcome message:
"""


@Cbot(pattern="^/welcome ?(.*)")
async def welfome(event):
    if event.is_private:
        return await event.reply("This command is made to used in group chats!")
    if not event.from_id:
        return await a_welcome(event, "welcome")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    settings = event.pattern_match.group(1)
    if not settings:
        chat_s = db.get_welcome(event.chat_id)
        if chat_s:
            re_to = await event.reply(w_str.format(chat_s["mode"]))
            file = idto_file(
                chat_s["id"], chat_s["hash"], chat_s["ref"], chat_s["mtype"]
            )
            r_text = chat_s["text"]
            if r_text:
                r_text, buttons = button_parser(r_text)
            await event.respond(r_text, file=file, buttons=buttons, reply_to=re_to.id)


@tbot.on(events.Raw(UpdateChannelParticipant))
async def cp(event):
    if event.prev_participant:
        return
    if not event.new_participant:
        return
    if isinstance(event.new_participant, ChannelParticipantBanned):
        return
    if isinstance(event.new_participant, ChannelParticipantAdmin):
        return
    chat_id = int(str(-100) + str(event.channel_id))
    cws = db.get_welcome(chat_id)
    first_name, last_name, mention, full_name, chat_id, id, title = await welcome_fill(
        event.user_id, chat_id
    )
    if not cws:
        return await tbot.send_message(chat_id, f"Hey **{first_name}**, How are you!")
    if cws["mode"] == False:
        return
    file = idto_file(cws["id"], cws["hash"], cws["ref"], cws["mtype"])
    r_text = cws["text"]
    if r_text:
        r_text, buttons = button_parser(r_text)
    await tbot.send_message(chat_id, r_text, buttons=buttons, file=file)


# add captcha
# add captcha buttons
# add other welcome tweaks
# afk for now
