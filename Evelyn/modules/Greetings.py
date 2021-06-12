from telethon import events
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantBanned,
    UpdateChannelParticipant,
)

import Evelyn.modules.sql.captcha_sql as cas
import Evelyn.modules.sql.welcome_sql as sql
from Evelyn import OWNER_ID, tbot
from Evelyn.events import Cbot

from . import button_parser, can_change_info, get_reply_msg_btns_text

wlc_st = """
I am currently welcoming users: `{}`
I am currently deleting old welcomes: `{}`
I am currently deleting service messages: `True`
CAPTCHAs are `{}`.
Welcome message:
"""
pos = ["yes", "y", "on"]
neg = ["n", "no", "off"]


@Cbot(pattern="^/welcome ?(.*)")
async def _(event):
    if event.is_private:
        return
    if event.is_group:
        if not event.sender_id == OWNER_ID:
            if not await can_change_info(event, event.sender_id):
                return
    args = event.pattern_match.group(1)
    if args.startswith("@"):
        args = None
    if not args:
        bstr = "False"
        welc = str(sql.welcome_mode(event.chat_id))
        cws = sql.get_current_welcome_settings(event.chat_id)
        welc_str = "Hey **{first_name}**, How are you."
        file = None
        if cws:
            welc_str = cws.custom_welcome_message
            if cws.should_clean_welcome is True:
                bstr = "True"
            file = cws.media_file_id
        mode = str(cas.get_mode(event.chat_id))
        k = await event.reply(wlc_st.format(welc, bstr, mode))
        welc_str, buttons = button_parser(welc_str)
        await k.reply(welc_str, parse_mode="html", buttons=buttons, file=file)
    elif args in pos:
        await event.reply("I'll be welcoming all new members from now on!")
        sql.set_welcome_mode(event.chat_id, True)
    elif args in neg:
        await event.reply("I'll stay quiet when new members join.")
        sql.set_welcome_mode(event.chat_id, False)
    elif args == "raw":
        welc_str = "Hey **{first_name}**, How are you."
        cws = sql.get_current_welcome_settings(event.chat_id)
        file = None
        if cws:
            welc_str = cws.custom_welcome_message
            file = cws.media_file_id
        await event.reply(welc_str, parse_mode=None, buttons=None, file=file)
    else:
        await event.reply("Your input was not recognised as one of: yes/no/on/off")


@Cbot(pattern="^/setwelcome ?(.*)")
async def _(event):
    if event.is_private:
        return
    if event.is_group:
        if not event.sender_id == OWNER_ID:
            if not await can_change_info(event, event.sender_id):
                return
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        return await event.reply("You need to give the welcome message some content!")
    elif event.reply_to_msg_id:
        msg = await event.get_reply_message()
        cws = sql.get_current_welcome_settings(event.chat_id)
        if cws:
            sql.rm_welcome_setting(event.chat_id)
        if msg.file:
            tbot_api_file_id = msg.file.id
            msg_message = msg.message
            if msg.reply_markup:
                btn_m = get_reply_msg_btns_text(msg)
                msg_message = str(msg_message) + str(btn_m)
            sql.add_welcome_setting(
                event.chat_id, msg_message, False, 0, tbot_api_file_id
            )
        else:
            sql.add_welcome_setting(event.chat_id, msg.message, False, 0, None)
    elif event.pattern_match.group(1):
        cws = sql.get_current_welcome_settings(event.chat_id)
        if cws:
            sql.rm_welcome_setting(event.chat_id)
        input_str = event.text.split(None, 1)
        sql.add_welcome_setting(event.chat_id, input_str[1], False, 0, None)
    await event.reply("The new welcome message has been saved!")
    sql.set_welcome_mode(event.chat_id, True)


neg_clean = """
I am not currently deleting old welcome messages when new members join.

To change this setting, try this command again followed by one of yes/no/on/off
"""
pos_clean = """
I am currently deleting old welcome messages when new members join.

To change this setting, try this command again followed by one of yes/no/on/off
"""


@Cbot(pattern="^/cleanwelcome ?(.*)")
async def cwlc(event):
    if event.is_private:
        return
    if event.is_group:
        if not event.sender_id == OWNER_ID:
            if not await can_change_info(event, event.sender_id):
                return
    args = event.pattern_match.group(1)
    if not args:
        cws = sql.get_current_welcome_settings(event.chat_id)
        if cws.should_clean_welcome:
            await event.reply(pos_clean)
        else:
            await event.reply(neg_clean)
    elif args in pos:
        await event.reply(
            "I'll be deleting all old welcome/goodbye messages from now on!"
        )
        sql.update_clean_welcome(event.chat_id, True)
    elif args in neg:
        await event.reply("I'll leave old welcome/goodbye messages.")
        sql.update_clean_welcome(event.chat_id, False)
    else:
        await event.reply("Your input was not recognised as one of: yes/no/on/off")


@tbot.on(events.Raw(UpdateChannelParticipant))
async def kek(event):
    try:
        if event.prev_participant:
            return
        if not event.new_participant:
            return
        if isinstance(event.new_participant, ChannelParticipantBanned):
            return
        if isinstance(event.new_participant, ChannelParticipantAdmin):
            return
        channel_id = str(-100) + str(event.channel_id)
        if not sql.welcome_mode(channel_id):
            return
        cws = sql.get_current_welcome_settings(int(channel_id))
        if cws:
            if cws.should_clean_welcome:
                message_id = cws.previous_welcome
                try:
                    await tbot.delete_messages(event.channel_id, [message_id])
                except:
                    sql.update_clean_welcome(int(channel_id), False)
        try:
            user = await tbot.get_entity(event.user_id)
            user_id = user.id
            bot = user.bot
            first_name = user.first_name
            last_name = user.last_name
            mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
            full_name = first_name
            if last_name:
                full_name = first_name + last_name
            username = user.username
            channel = await tbot.get_entity(event.channel_id)
            title = channel.title
            chat_id = event.channel_id
        except Exception as e:
            print(e)
            user_id = event.user_id
            first_name = "user"
            last_name = "user"
            full_name = "user"
            mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
            username = "@user"
            channel = await tbot.get_entity(event.channel_id)
            title = channel.title
            chat_id = event.channel_id
            bot = False
        if not cws:
            return await tbot.send_message(
                event.channel_id, f"Hey **{first_name}**, How are you."
            )
        custom_welcome = cws.custom_welcome_message
        if cas.get_mode(channel_id) == True:
            chat_info = channel_id
            if channel.username:
                chat_info = channel.username
            style = cas.get_style(channel_id)
            if style in ["math", "text"]:
                custom_welcome = (
                    custom_welcome
                    + f" [Click here to prove human](btnurl://t.me/MissEvelyn_Bot?start=captcha_{chat_info}&{style})"
                )
        welcome_text, buttons = button_parser(custom_welcome)
        welcome_text = welcome_text.format(
            mention=mention,
            first_name=first_name,
            last_name=last_name,
            username=username,
            chat_id=chat_id,
            full_name=full_name,
            title=title,
            id=user_id,
        )
        if cas.get_mode(channel_id) == True:
            if not bot:
                from .CAPTCHA import captcha_to_welcome

                return await captcha_to_welcome(event, welcome_text, None, buttons)
        file = None
        if cws.media_file_id:
            file = cws.media_file_id
        await tbot.send_message(
            event.channel_id,
            welcome_text,
            buttons=buttons,
            file=file,
            parse_mode="html",
        )
    except Exception as e:
        print(e)


@Cbot(pattern="^/goodbye ?(.*)")
async def db(event):
    if event.is_private:
        return
    if event.is_group:
        if not event.sender_id == OWNER_ID:
            if not await can_change_info(event, event.sender_id):
                return
    string_goodbye = """
I am currently saying goodbye to users: {}
I am currently deleting old goodbyes: {}
I am currently deleting service messages: {}

Members are currently bidden farewell with:
"""
    args = event.pattern_match.group(1)
    if args.startswith("@"):
        args = None
    if not args:
        wl_settings = str(sql.goodbye_mode(event.chat_id))
        cgs = sql.get_current_goodbye_settings(event.chat_id)
        if not cgs:
            no_cgs_str = "No custom goodbye message has been set; members are bidden farewell with:\n\nNice knowing you!"
            return await event.reply(no_cgs_str)
        if cgs:
            welc_str = cgs.custom_goodbye_message
            bstr = "False"
            if cgs.should_clean_goodbye is True:
                bstr = "True"
            res = await event.reply(string_goodbye.format(wl_settings, bstr, False))
            await res.reply(welc_str)
    elif args in pos:
        await event.reply("I'll be saying goodbye to any leavers from now on!")
        sql.set_goodbye_mode(event.chat_id, True)
    elif args in neg:
        await event.reply("I'll stay quiet when people leave.")
        sql.set_goodbye_mode(event.chat_id, False)
    else:
        await event.reply("Your input was not recognised as one of: yes/no/on/off")


@Cbot(pattern="^/setgoodbye ?(.*)")
async def gb(event):
    if event.is_private:
        return
    if event.is_group:
        if not event.sender_id == OWNER_ID:
            if not await can_change_info(event, event.sender_id):
                return
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        return await event.reply("You need to give the goodbye message some content!")
    elif event.reply_to_msg_id:
        msg = await event.get_reply_message()
        cws = sql.get_current_goodbye_settings(event.chat_id)
        if cws:
            sql.rm_goodbye_setting(event.chat_id)
        if msg.file:
            tbot_api_file_id = msg.file.id
            sql.add_goodbye_setting(
                event.chat_id, msg.message, False, 0, tbot_api_file_id
            )
        else:
            sql.add_goodbye_setting(event.chat_id, msg.message, False, 0, None)
    elif event.pattern_match.group(1):
        cws = sql.get_current_goodbye_settings(event.chat_id)
        if cws:
            sql.rm_goodbye_setting(event.chat_id)
        input_str = event.text.split(None, 1)
        sql.add_goodbye_setting(event.chat_id, input_str[1], False, 0, None)
    await event.reply("The new goodbye message has been saved!")
    sql.set_goodbye_mode(event.chat_id, True)


@tbot.on(events.Raw(UpdateChannelParticipant))
async def kek(event):
    try:
        if event.new_participant:
            return
        if isinstance(event.prev_participant, ChannelParticipantBanned):
            return
        if isinstance(event.prev_participant, ChannelParticipantAdmin):
            return
        channel_id = str(-100) + str(event.channel_id)
        if not sql.goodbye_mode(channel_id):
            return
        cgs = sql.get_current_goodbye_settings(int(channel_id))
        channel = await tbot.get_entity(event.channel_id)
        title = channel.title
        chat_id = event.channel_id
        try:
            user = await tbot.get_entity(event.user_id)
            user_id = user.id
            first_name = user.first_name
            last_name = user.last_name
            mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
            full_name = first_name
            if last_name:
                full_name = first_name + last_name
            username = user.username
        except:
            user_id = event.user_id
            first_name = "user"
            last_name = "user"
            full_name = "user"
            mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
            username = "@user"
        if not cgs:
            return await tbot.send_message(event.channel_id, f"Farewell {full_name}!")
        custom_goodbye = cgs.custom_goodbye_message
        goodbye_text, buttons = button_parser(custom_goodbye)
        goodbye_text = goodbye_text.format(
            mention=mention,
            first_name=first_name,
            last_name=last_name,
            username=username,
            chat_id=chat_id,
            full_name=full_name,
            title=title,
            id=user_id,
        )
        await tbot.send_message(
            event.channel_id,
            goodbye_text,
            buttons=buttons,
            file=None,
            parse_mode="html",
        )
    except Exception as e:
        print(e)


@Cbot(pattern="^/resetwelcome")
async def rwlc(event):
    if not event.is_group:
        return
    if event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    await event.reply("The welcome message has been reset to default!")
    sql.rm_welcome_setting(event.chat_id)


@Cbot(pattern="^/resetgoodbye")
async def rgb(event):
    if not event.is_group:
        return
    if event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    await event.reply("The goodbye message has been reset to default!")
    sql.rm_goodbye_setting(event.chat_id)


c_s_on = """
I am not currently deleting service messages when members join or leave.

To change this setting, try this command again followed by one of yes/no/on/off
"""
c_s_off = """
I am currently deleting service messages when new members join or leave.

To change this setting, try this command again followed by one of yes/no/on/off
"""


@Cbot(pattern="^/cleanservice ?(.*)")
async def rgb(event):
    if not event.is_group:
        return
    if event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    if event.chat.admin_rights:
        if not event.chat.admin_rights.delete_messages:
            return await event.reply(
                "Looks like I haven't got the right to delete messages; mind promoting me? Thanks!"
            )
    args = event.pattern_match.group(1)
    if not args:
        mode = sql.get_clean_service(event.chat_id)
        if mode:
            await event.reply(c_s_on)
        else:
            await event.reply(c_s_off)
    elif args in pos:
        await event.reply("I'll be deleting all service messages from now on!")
        sql.set_clean_service(event.chat_id, True)
    elif args in neg:
        sql.set_clean_service(event.chat_id, False)
        await event.reply("I'll leave service messages.")
    else:
        await event.reply("Your input was not recognised as one of: yes/no/on/off")


@tbot.on(events.ChatAction())
async def dlt_service(event):
    if not event.is_group:
        return
    if sql.get_clean_service(event.chat_id):
        if event.chat.admin_rights:
            if event.chat.admin_rights.delete_messages:
                await event.delete()
