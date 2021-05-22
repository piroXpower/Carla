from telethon import events

import Elsie.modules.sql.captcha_sql as cas
import Elsie.modules.sql.welcome_sql as sql
from Elsie import OWNER_ID, tbot
from Elsie.events import Cbot

from . import ELITES, button_parser, can_change_info

wlc_st = """
I am currently welcoming users: `{}`
I am currently deleting old welcomes: `{}`
I am currently deleting service messages: `True`
CAPTCHAs are `{}`.
"""
pos = ["yes", "y", "on"]
neg = ["n", "no", "off"]


@Cbot(pattern="^/welcome ?(.*)")
async def _(event):
    if event.is_private:
        return
    if not await can_change_info(event, event.sender_id):
        return
    args = event.pattern_match.group(1)
    if not args:
        bstr = "False"
        welc = str(sql.is_chat(event.chat_id))
        cws = sql.get_current_welcome_settings(event.chat_id)
        if cws:
            if cws.should_clean_welcome is True:
                bstr = "True"
        mode = str(cas.get_mode(event.chat_id))
        await event.reply(wlc_st.format(welc, bstr, mode))
    elif args in pos:
        await event.reply("I'll be welcoming all new members from now on!")
        sql.add_c(event.chat_id)
    elif args in neg:
        await event.reply("I'll stay quiet when new members join.")
        sql.rmc(event.chat_id)
    else:
        await event.reply("Your input was not recognised as one of: yes/no/on/off")


@Cbot(pattern="^/setwelcome ?(.*)")
async def _(event):
    if event.is_private:
        return
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


@tbot.on(events.ChatAction())
async def ca(event):
    if not event.user_joined and not event.user_added:
        return
    if not sql.is_chat(event.chat_id):
        return
    if event.user_id in ELITES:
        return await event.reply("An **ELITE** level disaster just joined. Beware.")
    elif event.user_id == OWNER_ID:
        return await event.reply("OwO, my **Owner** just joined!")
    cws = sql.get_current_welcome_settings(event.chat_id)
    if not cws:
        welcome_text = f"Hey **{event.user.first_name}**, How are you."
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
                    + f" [Click here to prove human](btnurl://t.me/MissElsie_Bot?start=captcha_{chat_info}&{style})"
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
        from .CAPTCHA import captcha_to_welcome

        return await captcha_to_welcome(event, welcome_text, file, buttons)
    await event.reply(welcome_text, buttons=buttons, file=file, parse_mode="htm")
