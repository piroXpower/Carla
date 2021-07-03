import datetime

from telethon import events
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantBanned,
    InputDocument,
    InputGeoPoint,
    InputMediaGeoPoint,
    MessageMediaDocument,
    MessageMediaGeo,
    MessageMediaPhoto,
    Photo,
    UpdateChannelParticipant,
)

import Jessica.modules.mongodb.welcome_db as db
import Jessica.modules.sql.captcha_sql as sql
from Jessica import CMD_HELP, tbot

from . import button_parser, can_change_info, get_reply_msg_btns_text


def get_fileids(r_msg):
    if isinstance(r_msg.media, MessageMediaDocument):
        file_id = r_msg.media.document.id
        access_hash = r_msg.media.document.access_hash
        file_reference = r_msg.media.document.file_reference
        type = "doc"
    elif isinstance(r_msg.media, MessageMediaPhoto):
        file_id = r_msg.media.photo.id
        access_hash = r_msg.media.photo.access_hash
        file_reference = r_msg.media.photo.file_reference
        type = "photo"
    elif isinstance(msg.media, MessageMediaGeo):
        file_id = msg.media.geo.long
        access_hash = msg.media.geo.lat
        file_reference = None
        type = "geo"
    else:
        return None, None, None, None
    return file_id, access_hash, file_reference, type


async def welcome_fill(chat_id, user_id):
    chat = await tbot.get_entity(chat_id)
    user = await tbot.get_entity(user_id)
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
    full_name = first_name
    if last_name:
        full_name = first_name + last_name
    id = user_id
    title = chat.title
    return first_name, last_name, mention, full_name, chat_id, id, title, username, chat.broadcast


def idto_file(id, hash, ref, type):
    if not id:
        return None
    elif type == "doc":
        return InputDocument(id=id, access_hash=hash, file_reference=ref)
    elif type == "photo":
        return Photo(
            id=file_id,
            access_hash=access_hash,
            file_reference=file_reference,
            date=datetime.datetime.now(),
            dc_id=5,
            sizes=[718118],
        )
    elif type == "geo":
        geo_file = InputMediaGeoPoint(InputGeoPoint(float(file_id), float(access_hash)))
        return geo_file


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
            if chat_s["text"] or chat_s["id"]:
                re_to = await event.reply(w_str.format(chat_s["mode"]))
                file = idto_file(
                    chat_s["id"], chat_s["hash"], chat_s["ref"], chat_s["mtype"]
                )
                r_text = chat_s["text"]
                if r_text:
                    r_text, buttons = button_parser(r_text)
                await event.respond(
                    r_text, file=file, buttons=buttons, reply_to=re_to.id
                )
            else:
                s_mode = True
                if chat_s and chat_s["mode"]:
                    s_mode = chat_s["mode"]
                re_to = await event.reply(w_str.format(s_mode))
                await event.respond("Hey {first_name}, how are you!", reply_to=re_to.id)
        else:
            re_to = await event.reply(w_str.format(True))
            await event.respond("Hey {first_name}, how are you!", reply_to=re_to.id)
    else:
        if settings in ["on", "yes", "y"]:
            db.toggle_welcome(event.chat_id, True)
            await event.reply("I'll be welcoming all new members from now on!")
        elif settings in ["off", "no", "n"]:
            db.toggle_welcome(event.chat_id, False)
            await event.reply("I'll stay quiet when new members join.")
        else:
            await event.reply("Your input was not recognised as one of: yes/no/on/off")


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
    if not db.get_welcome_mode(chat_id):
        return
    (
        first_name,
        last_name,
        mention,
        full_name,
        chat_id,
        id,
        title,
        username,
        channel,
    ) = await welcome_fill(chat_id, event.user_id)
    if channel and not cws:
         return
    if not cws:
        return await tbot.send_message(chat_id, f"Hey **{first_name}**, How are you!")
    if not cws["text"] and not cws["id"]:
        return await tbot.send_message(chat_id, f"Hey **{first_name}**, How are you!")
    file = idto_file(cws["id"], cws["hash"], cws["ref"], cws["mtype"])
    custom_welcome = cws["text"] or ""
    buttons = None
    welcome_text = ""
    if sql.get_mode(chat_id) == True:
        style = sql.get_style(chat_id)
        if style in ["math", "text"]:
            custom_welcome = (
                custom_welcome
                + f"[Click here to prove human](btnurl://t.me/MissNeko_Bot?start=captcha_{chat_id})"
            )
    if custom_welcome:
        welcome_text, buttons = button_parser(custom_welcome)
        welcome_text = welcome_text.format(
            fullname=full_name,
            title=title,
            chatname=title,
            id=id,
            chatid=chat_id,
            mention=mention,
            firstname=first_name,
            lastname=last_name,
            username=username,
        )
    if sql.get_mode(chat_id) == True:
        from .CAPTCHA import captcha_to_welcome

        return await captcha_to_welcome(event, welcome_text, file, buttons, chat_id)
    await tbot.send_message(chat_id, welcome_text, buttons=buttons, file=file)


@Cbot(pattern="^/setgoodbye ?(.*)")
async def set_gooxbye(event):
    if event.is_private:
        return await event.reply("nope")
    if not event.from_id:
        return await a_welcome(event, "setgoodbye")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    if not event.reply_to and not event.pattern_match.group(1):
        return await event.reply("You need to give the goodbye message some content!")
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
    await event.reply("The new goodbye message has been saved!")
    db.set_goodbye(event.chat_id, r_text, id, hash, ref, type)


@Cbot(pattern="^/resetgoodbye")
async def rw(event):
    if event.is_private:
        return await event.reply("This command is made to used in group chats!")
    if not event.from_id:
        return await a_welcome(event, "resetgoodbye")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    await event.reply("The goodbye message has been reset to default!")
    db.reset_goodbye(event.chat_id)


g_str = """
I am currently saying goodbye to users: {}
I am currently deleting old goodbyes: 
goodbye message:
"""


@Cbot(pattern="^/goodbye ?(.*)")
async def welfome(event):
    if event.is_private:
        return await event.reply("This command is made to used in group chats!")
    if not event.from_id:
        return await a_welcome(event, "goodbye")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    settings = event.pattern_match.group(1)
    if not settings:
        chat_s = db.get_goodbye(event.chat_id)
        if chat_s:
            if chat_s["text"] or chat_s["id"]:
                re_to = await event.reply(g_str.format(chat_s["mode"]))
                file = idto_file(
                    chat_s["id"], chat_s["hash"], chat_s["ref"], chat_s["mtype"]
                )
                buttons = None
                r_text = chat_s["text"]
                if r_text:
                    r_text, buttons = button_parser(r_text)
                await event.respond(
                    r_text, file=file, buttons=buttons, reply_to=re_to.id
                )
            else:
                s_mode = True
                if chat_s and chat_s["mode"]:
                    s_mode = chat_s["mode"]
                re_to = await event.reply(g_str.format(s_mode))
                await event.respond("Farewell {first_name}!", reply_to=re_to.id)
        else:
            re_to = await event.reply(h_str.format(True))
            await event.respond("Farewell {first_name}!", reply_to=re_to.id)
    else:
        if settings in ["on", "yes", "y"]:
            db.toggle_goodbye(event.chat_id, True)
            await event.reply("I'll be saying goodbye to any leavers from now on!")
        elif settings in ["off", "no", "n"]:
            db.toggle_goodbye(event.chat_id, False)
            await event.reply("I'll stay quiet when people leave.")
        else:
            await event.reply("Your input was not recognised as one of: yes/no/on/off")


@tbot.on(events.Raw(UpdateChannelParticipant))
async def cp(event):
    if event.new_participant:
        return
    if not event.prev_participant:
        return
    if isinstance(event.prev_participant, ChannelParticipantBanned):
        return
    if isinstance(event.prev_participant, ChannelParticipantAdmin):
        return
    chat_id = int(str(-100) + str(event.channel_id))
    cws = db.get_goodbye(chat_id)
    if not db.get_goodbye_mode(chat_id):
        return
    (
        first_name,
        last_name,
        mention,
        full_name,
        chat_id,
        id,
        title,
        username,
        channel,
    ) = await welcome_fill(chat_id, event.user_id)
    if channel and not cws:
       return
    if not cws:
        return await tbot.send_message(chat_id, f"Farewell {first_name}!")
    if not cws["text"] and not cws["id"]:
        return await tbot.send_message(chat_id, f"Farewell {first_name}!")
    file = idto_file(cws["id"], cws["hash"], cws["ref"], cws["mtype"])
    custom_goodbye = cws["text"] or ""
    goodbye_text = ""
    buttons = None
    if custom_goodbye:
        goodbye_text, buttons = button_parser(custom_goodbye)
        goodbye_text = goodbye_text.format(
            fullname=full_name,
            title=title,
            chatname=title,
            id=id,
            chatid=chat_id,
            mention=mention,
            firstname=first_name,
            lastname=last_name,
            username=username,
        )
    await tbot.send_message(chat_id, goodbye_text, buttons=buttons, file=file)


# add captcha
# add other welcome tweaks
# now working on notes
# and filters
async def a_welcome(event, mode):
    print(6)


__name__ = "greetings"
__help__ = """
**Welcome**
 - /welcome <on/off>: Enable or disable welcome messages.
 - /setwelcome <welcome message> or <reply to a text>: Saves the message as a welcome note in the chat.
 - /resetwelcome: Deletes the welcome note for the current chat.
 - /cleanwelcome <on/off>: Clean previous welcome message before welcoming a new user

**Goodbye**
 - /goodbye <on/off>: Enables or disables goodbye messages
 - /setgoodbye <goodbye message> or <reply to a text>: Saves the message as a goodbye note in the chat.
 - /resetgoodbye: Check whether you have a goodbye note in the chat.
 - /cleangoodbye <on/off>: Clean previous goodbye message before farewelling a new user

**Available variables for formatting greeting message:**
`{mention}, {title}, {count}, {firstname}, {fullname}, {username}, {chatid}, {lastname}, {id}, {chatname}`
"""

CMD_HELP.update({__name__: [__name__, __help__]})
