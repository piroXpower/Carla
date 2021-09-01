import datetime

from telethon import Button, events
from telethon.errors import ChannelPrivateError
from telethon.tl.functions.channels import GetFullChannelRequest
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

from .. import BOT_ID, CMD_HELP, tbot
from ..events import Cbot, Cinline
from . import button_parser, can_change_info, cb_can_change_info
from . import db as x_db
from . import get_reply_msg_btns_text
from .mongodb.chats_db import add_chat, is_chat

x_users = x_db.users
welcome_flood_control_db = {}
welcome_anon_db = {}


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
    elif isinstance(r_msg.media, MessageMediaGeo):
        file_id = r_msg.media.geo.long
        access_hash = r_msg.media.geo.lat
        file_reference = None
        type = "geo"
    else:
        return None, None, None, None
    return file_id, access_hash, file_reference, type


async def welcome_fill(chat_id, user_id):
    try:
        chat = await tbot.get_entity(chat_id)
        title = chat.title
        broadcast = chat.broadcast
    except ChannelPrivateError:
        title = "Chat"
        broadcast = True
    user = await tbot.get_entity(user_id)
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
    full_name = first_name
    if last_name:
        full_name = first_name + last_name
    id = user_id
    return (
        first_name,
        last_name,
        mention,
        full_name,
        chat_id,
        id,
        title,
        username,
        broadcast,
    )


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
            sizes=[7188],
        )
    elif type == "geo":
        geo_file = InputMediaGeoPoint(InputGeoPoint(float(file_id), float(access_hash)))
        return geo_file


@Cbot(pattern="^/setwelcome ?(.*)")
async def set_welxome(event):
    if event.is_private:
        return await event.reply("This command is made for group chats!")
    if not event.from_id:
        return await anon_welcome(event, "setwelcome")
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
        return await anon_welcome(event, "resetwelcome")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    await event.reply("The welcome message has been reset to default!")
    db.reset_welcome(event.chat_id)


@Cbot(pattern="^/welcome ?(.*)")
async def welxome_settings(event):
    if event.is_private:
        return await event.reply("This command is made to used in group chats!")
    if not event.from_id:
        return await anon_welcome(event, "welcome")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    settings = event.pattern_match.group(1)
    if not settings:
        chat_s = db.get_welcome(event.chat_id)
        welcome_str = """
I am currently welcoming users: {}
I am currently deleting old welcomes: 
I am currently deleting service messages: 
CAPTCHAs are .
Welcome message:
"""
        if chat_s:
            if chat_s["text"] or chat_s["id"]:
                re_to = await event.reply(welcome_str.format(chat_s["mode"]))
                file = idto_file(
                    chat_s["id"], chat_s["hash"], chat_s["ref"], chat_s["mtype"]
                )
                r_text = chat_s["text"]
                buttons = None
                if r_text:
                    r_text, buttons = button_parser(r_text)
                await event.respond(
                    r_text, file=file, buttons=buttons, reply_to=re_to.id
                )
            else:
                s_mode = True
                if chat_s and chat_s["mode"]:
                    s_mode = chat_s["mode"]
                re_to = await event.reply(welcome_str.format(s_mode))
                await event.respond("Hey {first_name}, how are you!", reply_to=re_to.id)
        else:
            re_to = await event.reply(welcome_str.format(True))
            await event.respond("Hey {first_name}, how are you!", reply_to=re_to.id)
    else:
        if settings in ["on", "yes", "y"]:
            db.toggle_welcome(event.chat_id, True)
            await event.reply("I'll be welcoming all new members from now on!")
        elif settings in ["off", "no", "n"]:
            db.toggle_welcome(event.chat_id, False)
            await event.reply("I'll stay quiet when new members join.")
        elif settings == "raw":
            chat_s = db.get_welcome(event.chat_id)
            if chat_s:
                file = idto_file(
                    chat_s["id"], chat_s["hash"], chat_s["ref"], chat_s["mtype"]
                )
                await event.reply(chat_s["text"], file=file)
        else:
            await event.reply("Your input was not recognised as one of: yes/no/on/off")


@tbot.on(events.Raw(UpdateChannelParticipant))
async def welcome_trigger(event):
    if event.prev_participant:
        return
    if not event.new_participant:
        return
    if isinstance(event.new_participant, ChannelParticipantBanned):
        return
    if isinstance(event.new_participant, ChannelParticipantAdmin):
        return
    chat_id = int(str(-100) + str(event.channel_id))
    try:
        welcome_ctrl = welcome_flood_control_db[chat_id]
        if (
            int((datetime.datetime.now() - welcome_ctrl[1]).total_seconds()) < 4
            and welcome_ctrl[0] >= 3
        ):
            return
    except KeyError:
        pass
    if event.user_id == BOT_ID:
        if not is_chat(chat_id):
            add_chat(chat_id)
        await tbot.send_message(
            chat_id,
            f"""Thanks for adding me to {(await tbot.get_entity(chat_id)).title}

Promote me as administrator in your group otherwise I will not function properly""",
            buttons=[
                [Button.url("Support Chat", "https://t.me/NekoChan_Support")],
                [Button.url("Updates Channel", "https://t.me/NekoChan_Updates")],
            ],
        )
        x = await tbot(GetFullChannelRequest(chat_id))
        current_count = x_users.find_one({"users": "main"})
        if current_count:
            total_count = current_count["users_count"] + x.full_chat.participants_count
        else:
            total_count = x.full_chat.participants_count
        return x_users.update_one(
            {"users": "main"}, {"$set": {"users_count": total_count}}, upsert=True
        )
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
    await tbot.send_message(
        chat_id, welcome_text, buttons=buttons, file=file, parse_mode="html"
    )
    try:
        X_MAX = welcome_flood_control_db[chat_id]
        X_key = X_MAX[0]
    except KeyError:
        X_key = 0
        X_MAX = None
    if X_MAX:
        if int((datetime.datetime.now() - X_MAX[1]).total_seconds()) < 4:
            chance = X_key + 1
        else:
            chance = 0
    else:
        chance = 0
    welcome_flood_control_db[chat_id] = [chance, datetime.datetime.now()]


@Cbot(pattern="^/setgoodbye ?(.*)")
async def set_gooxbye(event):
    if event.is_private:
        return await event.reply("This command is made to used in group chats!")
    if not event.from_id:
        return await anon_welcome(event, "setgoodbye")
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
        return await anon_welcome(event, "resetgoodbye")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    await event.reply("The goodbye message has been reset to default!")
    db.reset_goodbye(event.chat_id)


@Cbot(pattern="^/goodbye ?(.*)")
async def welfome(event):
    if event.is_private:
        return await event.reply("This command is made to used in group chats!")
    if not event.from_id:
        return await anon_welcome(event, "goodbye")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    settings = event.pattern_match.group(1)
    if not settings:
        goodbye_str = """
I am currently saying goodbye to users: {}
I am currently deleting old goodbyes: {}
goodbye message:
"""
        chat_s = db.get_goodbye(event.chat_id)
        if chat_s:
            if chat_s["text"] or chat_s["id"]:
                re_to = await event.reply(goodbye_str.format(chat_s["mode"]))
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
                re_to = await event.reply(goodbye_str.format(s_mode))
                await event.respond("Farewell {first_name}!", reply_to=re_to.id)
        else:
            re_to = await event.reply(goodbye_str.format(True, False))
            await event.respond("Farewell {first_name}!", reply_to=re_to.id)
    else:
        if settings in ["on", "yes", "y"]:
            await event.reply("I'll be saying goodbye to any leavers from now on!")
            db.toggle_goodbye(event.chat_id, True)
        elif settings in ["off", "no", "n"]:
            await event.reply("I'll stay quiet when people leave.")
            db.toggle_goodbye(event.chat_id, False)
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
    await tbot.send_message(
        chat_id, goodbye_text, buttons=buttons, file=file, parse_mode="html"
    )


x_false = """
I am not currently deleting service messages when members join or leave.

To change this setting, try this command again followed by one of yes/no/on/off
"""
x_true = """
I am currently deleting service messages when new members join or leave.

To change this setting, try this command again followed by one of yes/no/on/off
"""


@Cbot(pattern="^/cleanservice ?(.*)")
async def clean_service(e):
    if e.is_private:
        return await e.reply("This command is made to used in group chats!")
    if not e.from_id:
        return await anon_welcome(e, "cleanservice")
    if e.is_group:
        if not await can_change_info(e, e.sender_id):
            return
    args = e.pattern_match.group(1)
    if not args:
        settings = db.get_clean_service(e.chat_id)
        if settings:
            await e.reply(x_true)
        else:
            await e.reply(x_false)
    elif args in ["on", "yes", "y"]:
        await e.reply("I'll be deleting all service messages from now on!")
        db.set_clean_service(e.chat_id, True)
    elif args in ["off", "no", "n"]:
        await e.reply("I'll leave service messages.")
        db.set_clean_service(e.chat_id, False)
    else:
        await e.reply("Your input was not recognised as one of: yes/no/on/off")


@tbot.on(events.ChatAction())
async def clean_service(e):
    if e.is_private:
        return
    d = db.get_clean_service(e.chat_id)
    if not d:
        return
    if e.user_joined or e.user_added:
        if e.chat.admin_rights:
            if e.chat.admin_rights.delete_messages:
                await e.delete()


# --------Anonymous_Admins---------
async def anon_welcome(e, mode):
    if e.reply_to:
        mode_text = (await e.get_reply_message()).text or "None"
    elif e.pattern_match.group(1):
        mode_text = e.text.split(None, 1)[1]
    else:
        mode_text = "None"
    welcome_anon_db[e.id] = mode_text
    cb_data = str(e.id) + "|" + mode
    x_buttons = Button.inline(
        "Click to prove Admin", data="x_welcome_{}".format(cb_data)
    )
    await e.reply(
        "It looks like you're anonymous. Tap this button to confirm your identity.",
        buttons=x_buttons,
    )


@Cinline(pattern="x_welcome(\_(.*))")
async def x_welcome(e):
    x_data = (((e.pattern_match.group(1)).decode()).split("_", 1)[1]).split("|", 1)
    x_event_id = int(x_data[0])
    x_mode = x_data[1]
    if not await cb_can_change_info(e, e.sender_id):
        return
    try:
        x_cb_data = welcome_anon_db[x_event_id]
    except KeyError:
        return await e.edit("This Request Has Been Expired!", buttons=None)
    if x_mode == "welcome":
        if x_cb_data == "None":
            chat_s = db.get_welcome(e.chat_id)
            welcome_str = """
I am currently welcoming users: {}
I am currently deleting old welcomes: 
I am currently deleting service messages: 
CAPTCHAs are .
Welcome message:
"""
            if chat_s:
                if chat_s["text"] or chat_s["id"]:
                    re_to = await e.edit(welcome_str.format(chat_s["mode"]))
                    file = idto_file(
                        chat_s["id"], chat_s["hash"], chat_s["ref"], chat_s["mtype"]
                    )
                    r_text = chat_s["text"]
                    if r_text:
                        r_text, buttons = button_parser(r_text)
                    await e.respond(
                        r_text, file=file, buttons=buttons, reply_to=re_to.id
                    )
                else:
                    s_mode = True
                    if chat_s and chat_s["mode"]:
                        s_mode = chat_s["mode"]
                    re_to = await e.edit(welcome_str.format(s_mode))
                    await e.respond("Hey {first_name}, how are you!", reply_to=re_to.id)
            else:
                re_to = await e.reply(welcome_str.format(True))
                await e.respond("Hey {first_name}, how are you!", reply_to=re_to.id)
        elif x_cb_data in ["on", "yes", "y"]:
            db.toggle_welcome(e.chat_id, True)
            await e.edit("I'll be welcoming all new members from now on!")
        elif x_cb_data in ["off", "no", "n"]:
            db.toggle_welcome(e.chat_id, False)
            await e.edit("I'll stay quiet when new members join.")
        else:
            await e.edit("Your input was not recognised as one of: yes/no/on/off")
    elif x_mode == "setwelcome":
        if x_cb_data == "None":
            return await e.edit("You need to give the welcome message some content!")
        else:
            await e.edit("The new welcome message has been saved!")
            db.set_welcome(e.chat_id, x_cb_data, None, None, None, None)
    elif x_mode == "resetwelcome":
        await e.edit("The welcome message has been reset to default!")
        db.reset_welcome(e.chat_id)
    elif x_mode == "goodbye":
        if x_cb_data == "None":
            chat_s = db.get_goodbye(e.chat_id)
            goodbye_str = """
I am currently saying goodbye to users: {}
I am currently deleting old goodbyes: {}
goodbye message:
"""
            if chat_s:
                if chat_s["text"] or chat_s["id"]:
                    re_to = await e.edit(goodbye_str.format(chat_s["mode"]))
                    file = idto_file(
                        chat_s["id"], chat_s["hash"], chat_s["ref"], chat_s["mtype"]
                    )
                    r_text = chat_s["text"]
                    if r_text:
                        r_text, buttons = button_parser(r_text)
                    await e.respond(
                        r_text, file=file, buttons=buttons, reply_to=re_to.id
                    )
                else:
                    s_mode = True
                    if chat_s and chat_s["mode"]:
                        s_mode = chat_s["mode"]
                    re_to = await e.edit(goodbye_str.format(s_mode))
                    await e.respond("FareWell {first_name}", reply_to=re_to.id)
            else:
                re_to = await e.edit(goodbye_str.format(True))
                await e.respond("FareWell {first_name}", reply_to=re_to.id)
        elif x_cb_data in ["on", "yes", "y"]:
            await e.edit("I'll be saying goodbye to any leavers from now on!")
            db.toggle_goodbye(e.chat_id, True)
        elif x_cb_data in ["off", "no", "n"]:
            await e.edit("I'll stay quiet when people leave.")
            db.toggle_goodbye(e.chat_id, False)
        else:
            await e.edit("Your input was not recognised as one of: yes/no/on/off")
    elif x_mode == "setgoodbye":
        if x_cb_data == "None":
            return await e.edit("You need to give the welcome message some content!")
        else:
            await e.edit("The new goodbye message has been saved!")
            db.set_goodbye(e.chat_id, x_cb_data, None, None, None, None)
    elif x_mode == "resetgoodbye":
        await e.edit("The goodbye message has been reset to default!")
        db.reset_goodbye(e.chat_id)
    elif x_mode == "cleanservice":
        if x_cb_data == "None":
            settings = db.get_clean_service(e.chat_id)
            if settings:
                await e.edit(x_true)
            else:
                await e.edit(x_false)
    del welcome_flood_control_db[x_event_id]


# balance soon

__name__ = "greetings"
__help__ = """
Here is the help for **Greetings** module:

**Welcome**
-> /welcome `<on/off>`
Enable or disable welcome messages.
-> /setwelcome `<welcome message>` or `<reply>
Saves the message as a welcome note in the chat.
-> /resetwelcome
Deletes the welcome note for the current chat.
-> /cleanwelcome `<on/off>`
Clean previous welcome message before welcoming a new user
-> /cleanservice `<on/off>`
Clean service messages.

**Goodbye**
-> /goodbye `<on/off>`
Enables or disables goodbye messages
-> /setgoodbye `<goodbye message>` or `<reply>`
Saves the message as a goodbye note in the chat.
-> /resetgoodbye
Check whether you have a goodbye note in the chat.
-> /cleangoodbye `<on/off>`
Clean previous goodbye message before farewelling a new user

**Available variables for formatting greeting message:**
`{mention}`, `{title}`, `{count}`, `{firstname}`, `{fullname}`, `{username}`, `{chatid}`, `{lastname}`, `{id}`, `{chatname}`
"""

CMD_HELP.update({__name__: [__name__, __help__]})
