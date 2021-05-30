from telethon import events
from telethon.tl.types import ChannelParticipantBanned, UpdateChannelParticipant

import Evelyn.modules.sql.captcha_sql as cas
import Evelyn.modules.sql.welcome_sql as sql
from Evelyn import OWNER_ID, tbot
from Evelyn.events import Cbot

from . import ELITES, button_parser, can_change_info

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
        if cws:
            welc_str = cws.custom_welcome_message
            if cws.should_clean_welcome is True:
                bstr = "True"
        mode = str(cas.get_mode(event.chat_id))
        k = await event.reply(wlc_st.format(welc, bstr, mode))
        await k.reply(welc_str)
    elif args in pos:
        await event.reply("I'll be welcoming all new members from now on!")
        sql.set_welcome_mode(event.chat_id, True)
    elif args in neg:
        await event.reply("I'll stay quiet when new members join.")
        sql.set_welcome_mode(event.chat_id, False)
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
            sql.add_welcome_setting(
                event.chat_id, msg.message, False, 0, tbot_api_file_id
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

@tbot.on(events.ChatAction())
async def ca(event):
    if not event.user_joined and not event.user_added:
        return
    if not sql.welcome_mode(event.chat_id):
        return
    if event.user_id in ELITES:
        return await event.reply("An **ELITE** level disaster just joined. Beware.")
    elif event.user_id == OWNER_ID:
        return await event.reply("OwO, my **Owner** just joined!")
    cws = sql.get_current_welcome_settings(event.chat_id)
    if not cws:
        welcome_text = f"Hey **{event.user.first_name}**, How are you!"
        buttons = []
        file = None
    else:
        custom_welcome = cws.custom_welcome_message
        if cas.get_mode(event.chat_id) == True:
            chat_info = event.chat_id
            if event.chat.username:
                chat_info = event.chat.username
            style = cas.get_style(event.chat_id)
            if style in ["math", "text"]:
                custom_welcome = (
                    custom_welcome
                    + f" [Click here to prove human](btnurl://t.me/MissEvelyn_Bot?start=captcha_{chat_info}&{style})"
                )
        welcome_text, buttons = button_parser(custom_welcome)
        first_name = event.user.first_name
        last_name = event.user.last_name
        if last_name:
            full_name = first_name + last_name
        else:
            full_name = first_name
        user_id = event.user_id
        chat_title = event.chat.title
        chat_id = event.chat_id
        chat_username = event.chat.username
        username = event.user.username
        mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
        welcome_text = welcome_text.format(
            mention=mention,
            first_name=first_name,
            last_name=last_name,
            username=username,
            chat_id=chat_id,
            chat_username=chat_username,
            full_name=full_name,
            chat_title=chat_title,
            id=user_id,
        )
        file = None
    if cas.get_mode(event.chat_id) == True:
        if not event.user.bot:
            from .CAPTCHA import captcha_to_welcome

            return await captcha_to_welcome(event, welcome_text, file, buttons)
    await event.reply(welcome_text, buttons=buttons, file=file, parse_mode="htm")


@tbot.on(events.Raw())
async def kek(event):
    try:
        if not isinstance(event, UpdateChannelParticipant):
            return
        if event.prev_participant:
            return
        if not event.new_participant:
            return
        if isinstance(event.new_participant, ChannelParticipantBanned):
            return
        channel_id = str(-100) + str(event.channel_id)
        if not sql.goodbye_mode(channel_id):
            return
        cws = sql.get_current_welcome_settings(int(channel_id))
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
        if not cws:
            return await tbot.send_message(
                event.channel_id, f"Hey **{first_name}**, How are you."
            )
        custom_welcome = cws.custom_welcome_message
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
        await tbot.send_message(
            event.channel_id,
            welcome_text,
            buttons=buttons,
            file=None,
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
    
@tbot.on(events.Raw())
async def kek(event):
    if not isinstance(event, UpdateChannelParticipant):
        return
    if event.new_participant:
        return
    if isinstance(event.prev_participant, ChannelParticipantBanned):
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
    custom_goodbye = cws.custom_goodbye_message
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
