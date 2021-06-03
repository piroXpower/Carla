import re
import time

from telethon import Button, events

import Evelyn.modules.sql.blacklist_sql as sql
import Evelyn.modules.sql.warns_sql as wsql
from Evelyn import OWNER_ID, tbot
from Evelyn.events import Cbot

from . import ELITES, can_change_info, extract_time, is_admin, is_owner


@Cbot(pattern="^/addblocklist ?(.*)")
async def _(event):
    if event.is_private:
        return  # connect
    if not event.from_id:
        return
    if not await can_change_info(event, event.sender_id):
        return
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        trigger = msg.message
    elif event.pattern_match.group(1):
        trigger = event.pattern_match.group(1)
    else:
        return await event.reply(
            "You need to provide a blocklist trigger!\neg: `/addblocklist the admins suck`."
        )
    if len(trigger) > 33:
        return await event.reply("The BlackList filter is too long!")
    text = "Added blocklist filter '{}'!".format(trigger)
    await event.respond(text)
    sql.add_to_blacklist(event.chat_id, trigger)


@Cbot(pattern="^/addblacklist ?(.*)")
async def _(event):
    if event.is_private:
        return  # connect
    if not event.from_id:
        return
    if not await can_change_info(event, event.sender_id):
        return
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        trigger = msg.message
    elif event.pattern_match.group(1):
        trigger = event.pattern_match.group(1)
    else:
        return await event.reply(
            "You need to provide a blocklist trigger!\neg: `/addblocklist the admins suck`."
        )
    if len(trigger) > 33:
        return await event.reply("The BlackList filter is too long!")
    text = "Added blocklist filter '{}'!".format(trigger)
    await event.respond(text)
    sql.add_to_blacklist(event.chat_id, trigger)


@Cbot(pattern="^/(blocklist|blacklist)$")
async def _(event):
    if event.is_private:
        return  # connect
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("You need to be an admin to do this.")
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    if len(all_blacklisted) == 0:
        text = "No blocklist filters active in {}!".format(event.chat.title)
    else:
        text = "The following blocklist filters are currently active in {}:".format(
            event.chat.title
        )
        for i in all_blacklisted:
            text += f"\n- `{i}`"
    await event.reply(text)


@Cbot(pattern="^/(rmblacklist|rmblocklist) ?(.*)")
async def _(event):
    if event.is_private:
        return  # connect
    if not await can_change_info(event, event.sender_id):
        return
    args = event.pattern_match.group(2)
    if not args:
        return await event.reply("You need to specify the blocklist filter to remove")
    d = sql.rm_from_blacklist(event.chat_id, args)
    if d:
        text = "I will no longer blocklist '{}'.".format(args)
    else:
        text = f"`{args}` has not been blocklisted, and so could not be stopped. Use the /blocklist command to see the current blocklist."
    await event.reply(text)


@Cbot(pattern="^/(unblocklistall|unblacklistall)$")
async def _(event):
    if event.is_private:
        return  # connect
    if not await is_owner(event, event.sender_id):
        return
    buttons = [Button.inline("Delete blocklist", data="dabl")], [
        Button.inline("Cancel", data="cabl")
    ]
    text = "Are you sure you would like to stop **ALL** of the blocklist in {}? This action cannot be undone.".format(
        event.chat.title
    )
    await event.reply(text, buttons=buttons)


@tbot.on(events.CallbackQuery(pattern="dabl"))
async def dabl(event):
    perm = await tbot.get_permissions(event.chat_id, event.sender_id)
    if not perm.is_admin:
        return await event.answer("You need to be an admin.")
    if not perm.is_creator:
        return await event.answer("You need to be the chat creator.")
    await event.edit("Deleted chat blocklist.")
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    for i in all_blacklisted:
        sql.rm_from_blacklist(event.chat_id, str(i))


@tbot.on(events.CallbackQuery(pattern="cabl"))
async def cabl(event):
    perm = await tbot.get_permissions(event.chat_id, event.sender_id)
    if not perm.is_admin:
        return await event.answer("You need to be an admin.")
    if not perm.is_creator:
        return await event.answer("You need to be the chat creator.")
    await event.edit("Removal of the blocklist has been cancelled.")


addon = """

If you want to change this setting, you will need to specify an action to take on blocklisted words. Possible modes are: nothing/ban/mute/kick/warn/tban/tmute
"""
Geys = """
It looks like you tried to set time value for blacklist but you didn't specified  time; try, `/blacklistmode tmute/tban <timevalue>`.

Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""


@Cbot(pattern="^/(blocklistmode|blacklistmode) ?(.*)")
async def _(event):
    if event.is_private:
        return  # connect
    if not await can_change_info(event, event.sender_id):
        return
    args = event.pattern_match.group(2)
    if not args:
        mode = sql.get_mode(event.chat_id)
        if mode == "nothing":
            text = "Your current blocklist preference is just to delete messages with blocklisted words."
        elif mode == "warn":
            text = "Your current blocklist preference is to warn users on messages containing blocklisted words, and delete the message."
        elif mode == "ban":
            text = "Your current blocklist preference is to ban users on messages containing blocklisted words, and delete the message."
        elif mode == "mute":
            text = "Your current blocklist preference is to mute users on messages containing blocklisted words, and delete the message."
        elif mode == "kick":
            text = "Your current blocklist preference is to kick users on messages containing blocklisted words, and delete the message."
        elif mode == "tban":
            text = "Your current blocklist preference is to tban users on messages containing blocklisted words, and delete the message."
        elif mode == "tmute":
            text = "Your current blocklist preference is to tmute users on messages containing blocklisted words, and delete the message."
        await event.reply(text + addon)
    else:
        lolz = args
        args = args.split()
        if not args[0] in ["ban", "mute", "kick", "tban", "tmute", "nothing", "warn"]:
            return await event.reply(
                f"Unknown type {args[0]}. Please use one of: nothing/ban/mute/kick/warn/tban/tmute"
            )
        if args[0] in ["tban", "tmute"]:
            if len(args) == 1:
                return await event.reply(Geys)
            time = await extract_time(event, args[1])
            sql.set_time(event.chat_id, time)
            sql.add_mode(event.chat_id, args[0])
            if args[0] == "tban":
                text = f"Changed blacklist mode: temporarily ban for {lolz}!"
            elif args[0] == "tmute":
                text = f"Changed blacklist mode: temporarily mute for {lolz}!"
        else:
            sql.add_mode(event.chat_id, args[0])
            text = f"Changed blacklist mode: {args[0]} the sender!"
        await event.respond(text)


@tbot.on(events.NewMessage(incoming=True))
async def on_new_message(event):
    if event.is_private:
        return  # connect
    if not event.from_id:
        return
    if (
        event.sender_id in ELITES
        or event.sender_id == OWNER_ID
        or await is_admin(event.chat_id, event.sender_id)
    ):
        return  # admins
    if event.media:
        return
    name = event.text
    snips = sql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            await event.delete()
            mode = sql.get_mode(event.chat_id)
            if mode == "nothing":
                return
            elif mode == "ban":
                await tbot.edit_permissions(
                    event.chat_id, event.sender_id, until_date=None, view_messages=False
                )
                await event.respond(
                    f"Banned **{event.sender.first_name}**\nReason: Automated blacklist action, due to a match on '{name}'"
                )
            elif mode == "kick":
                await tbot.kick_participant(event.chat_id, event.sender_id)
            elif mode == "mute":
                await tbot.edit_permissions(
                    event.chat_id, event.sender_id, until_date=None, send_messages=False
                )
            elif mode == "tban":
                tt = sql.get_time(event.chat_id)
                await tbot.edit_permissions(
                    event.chat_id,
                    event.sender_id,
                    until_date=time.time() + int(tt),
                    view_messages=False,
                )
            elif mode == "tmute":
                tt = sql.get_time(event.chat_id)
                await tbot.edit_permissions(
                    event.chat_id,
                    event.sender_id,
                    until_date=time.time() + int(tt),
                    send_messages=False,
                )
            elif mode == "warn":
                await block_list_warn(event, name)


async def block_list_warn(event, name):
    text = f"Reason: Automated blacklist action, due to a match on '{name}'"
    limit = wsql.get_limit(event.chat_id)
    num_warns, reasons = wsql.warn_user(event.sender_id, event.chat_id, text)
    if num_warns < limit:
        f"{event.chat_id}-{event.sender_id}"
        liz = "User [{}](tg://user?id={}) has {}/{} warnings; be careful!.\n{}".format(
            event.sender.first_name, event.sender_id, num_warns, limit, text
        )
        buttons = [Button.inline("Remove warn", data=f"rm_warn-{event.sender_id}")]
        await event.respond(liz, buttons=buttons)
    else:
        wsql.reset_warns(event.sender_id, event.chat_id)
        action = wsql.get_warn_strength(event.chat_id)
        if action == "ban":
            await event.respond(
                "Thats {}/{} warnings. [{}](tg://user?id={}) has been Banned!\n{}".format(
                    limit, limit, event.sender.first_name, event.sender_id, text
                )
            )
            await tbot.edit_permissions(
                event.chat_id, event.sender_id, until_date=None, view_messages=False
            )
        elif action == "kick":
            await event.respond(
                "Thats {}/{} warnings. [{}](tg://user?id={}) has been Kicked!\n{}".format(
                    limit, limit, event.sender.first_name, event.sender_id, text
                )
            )
            await tbot.kick_participant(event.chat_id, event.sender_id)
        elif action == "mute":
            await event.respond(
                "Thats {}/{} warnings. [{}](tg://user?id={}) has been Muted!\n{}".format(
                    limit, limit, event.sender.first_name, event.sender_id, text
                )
            )
            await tbot.edit_permissions(
                event.chat_id, event.sender_id, until_date=None, send_messages=False
            )
        elif action == "tban":
            time = wsql.get_ban_time(event.chat_id)
            await event.respond(
                "Thats {}/{} warnings. [{}](tg://user?id={}) has been Temporarily Banned!\n{}".format(
                    limit, limit, event.sender.first_name, event.sender_id, text
                )
            )
            await tbot.edit_permissions(
                event.chat_id,
                event.sender_id,
                until_date=time.time() + int(time),
                view_messages=False,
            )
        elif action == "tmute":
            await event.respond(
                "Thats {}/{} warnings. [{}](tg://user?id={}) has been Temporarily Muted!\n{}".format(
                    limit, limit, event.sender.first_name, event.sender_id, text
                )
            )
            await tbot.edit_permissions(
                event.chat_id,
                event.sender_id,
                until_date=time.time() + int(time),
                send_messages=False,
            )
