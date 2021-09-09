import re
import time

from telethon import Button, events
from telethon.tl.types import PeerChannel

import neko.modules.sql.blacklist_sql as sql
import neko.modules.sql.warns_sql as wsql
from neko import OWNER_ID, tbot
from neko.utils import Cbot, Cinline

from . import DEVS, can_change_info, cb_is_owner, extract_time, is_admin, is_owner
from .mongodb import blacklist_db as db


@Cbot(pattern="^/addblocklist ?(.*)")
async def _(event):
    if event.is_private:
        return await event.reply("Thid command is made for group chats, not my PM!")
    if not event.from_id:
        return
    if not await can_change_info(event, event.sender_id):
        return
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        trigger = msg.text.split(None, 1)[0]
    elif event.pattern_match.group(1):
        trigger = event.text.split(None, 1)[1]
    else:
        return await event.reply(
            "You need to provide a blocklist trigger!\neg: `/addblocklist the admins suck`."
        )
    if len(trigger) > 33:
        return await event.reply("The BlackList filter is too long!")
    text = "Added blocklist filter '{}'!".format(trigger)
    await event.reply(text)
    db.add_to_blacklist(event.chat_id, trigger)


@Cbot(pattern="^/addblacklist ?(.*)")
async def _(event):
    if event.is_private:
        return await event.reply("Thid command is made for group chats, not my PM!")
    if not event.from_id:
        return
    if not await can_change_info(event, event.sender_id):
        return
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        trigger = msg.message
    elif event.pattern_match.group(1):
        trigger = event.text.split(None, 1)[1]
    else:
        return await event.reply(
            "You need to provide a blocklist trigger!\neg: `/addblocklist the admins suck`."
        )
    if len(trigger) > 20:
        return await event.reply("The BlackList filter is too long!")
    text = "Added blocklist filter '{}'!".format(trigger)
    await event.reply(text)
    db.add_to_blacklist(event.chat_id, trigger)


@Cbot(pattern="^/(blocklist|blacklist)$")
async def _(event):
    if event.is_private:
        return  # connect
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("You need to be an admin to do this.")
    all_blacklisted = db.get_chat_blacklist(event.chat_id)
    if (all_blacklisted and len(all_blacklisted) == 0) or not all_blacklisted:
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
    d = db.rm_from_blacklist(event.chat_id, args)
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


@Cinline(pattern="dabl")
async def dabl(event):
    if not await cb_is_owner(event, event.sender_id):
        return
    await event.edit("Deleted all chat blocklist filters.")
    db.remove_all_blacklist(event.chat_id)


@Cinline(pattern="cabl")
async def cabl(event):
    if not await cb_is_owner(event, event.sender_id):
        return
    await event.edit("Removal of the all chat blocklist filters has been cancelled.")


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
        mode, time = db.get_mode(event.chat_id)
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
            db.set_mode(event.chat_id, args[0], time)
            if args[0] == "tban":
                text = f"Changed blacklist mode: temporarily ban for {lolz}!"
            elif args[0] == "tmute":
                text = f"Changed blacklist mode: temporarily mute for {lolz}!"
        else:
            db.set_mode(event.chat_id, args[0])
            text = f"Changed blacklist mode: {args[0]} the sender!"
        await event.reply(text)


@tbot.on(events.NewMessage(incoming=True))
async def on_new_message(event):
    if event.is_private:
        return
    if not event.from_id:
        return
    if isinstance(event.from_id, PeerChannel) or event.fwd_from or event.media:
        return
    name = event.text
    trigg = False
    snips = db.get_chat_blacklist(event.chat_id)
    if not snips:
        return
    snip_t = ""
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            trigg = True
            snip_t = snip
    if trigg:
        if (
            event.sender_id in DEVS
            or event.sender_id == OWNER_ID
            or await is_admin(event.chat_id, event.sender_id)
        ):
            return  # admins
        await blocklist_action(event, snip_t)


async def blocklist_action(event, name):
    await event.delete()
    mode, ban_time = db.get_mode(event.chat_id)
    if mode == "nothing":
        return
    elif mode == "ban":
        task = "Banned"
        await tbot.edit_permissions(
            event.chat_id, event.sender_id, until_date=None, view_messages=False
        )
    elif mode == "kick":
        task = "Kicked"
        await tbot.kick_participant(event.chat_id, event.sender_id)
    elif mode == "mute":
        task = "Muted"
        await tbot.edit_permissions(
            event.chat_id, event.sender_id, until_date=None, send_messages=False
        )
    elif mode == "tban":
        task = "Banned"
        await tbot.edit_permissions(
            event.chat_id,
            event.sender_id,
            until_date=time.time() + int(ban_time),
            view_messages=False,
        )
    elif mode == "tmute":
        task = "Muted"
        await tbot.edit_permissions(
            event.chat_id,
            event.sender_id,
            until_date=time.time() + int(ban_time),
            send_messages=False,
        )
    elif mode == "warn":
        await bl_warn(
            event.chat_id, event.sender.first_name, event.sender_id, event.id, name
        )
    if mode in ["ban", "mute", "kick", "tban", "tmute"]:
        await event.respond(
            "[{}](tg://user?id={}) has been {}!\nReason: `Automatic blacklist action, due to match on {}`".format(
                event.sender.first_name, event.sender_id, task, name
            )
        )


async def bl_warn(chat_id, first_name, user_id, reply_id, name):
    limit = wsql.get_limit(chat_id)
    num_warns, reasons = wsql.warn_user(
        user_id, chat_id, f"Automatic blocklist action, due to a match on {name}"
    )
    if num_warns < limit:
        await tbot.send_message(
            chat_id,
            "User [{}](tg://user?id={}) has {}/{} warnings; be careful!.\nReason: `Automatic blacklist action, due to match on {}`".format(
                first_name, user_id, num_warns, limit, name
            ),
            buttons=Button.inline(
                "Remove warn (admin only)", data=f"rm_warn-{user_id}"
            ),
            reply_to=reply_id,
        )
    else:
        wsql.reset_warns(usee_id, chat_id)
        mode = wsql.get_warn_strength(chat_id)
        if mode == "ban":
            task = "Banned"
            await tbot.edit_permissions(
                chat_id, user_id, until_date=None, view_messages=False
            )
        elif mode == "kick":
            task = "Kicked"
            await tbot.kick_participant(chat_id, user_id)
        elif mode == "mute":
            task = "Muted"
            await tbot.edit_permissions(
                chat_id, user_id, until_date=None, send_messages=False
            )
        elif mode == "tban":
            task = "Banned"
            ban_time = int(sql.get_time(event.chat_id))
            await tbot.edit_permissions(
                chat_id,
                user_id,
                until_date=time.time() + ban_time,
                view_messages=False,
            )
        elif mode == "tmute":
            task = "Muted"
            mute_time = int(sql.get_time(event.chat_id))
            await tbot.edit_permissions(
                chat_id,
                user_id,
                until_date=time.time() + mute_time,
                send_messages=False,
            )
        await tbot.send_message(
            chat_id,
            "Thats {}/{} warnings. [{}](tg://user?id={}) has been {}!\nReason: `Automatic blacklist action, due to match on {}`".format(
                limit, limit, first_name, user_id, task, name
            ),
            reply_to=reply_id,
        )


# add blocklistdelete, setblocklistreason, resetblocklistreason
# while shifiting db to mongodb

__help__ = """
Blocklists

Want to stop people asking stupid questions? or ban anyone saying censored words? Blocklists is the module for you!

From blocking rude words, filenames/extensions, to specific emoji, everything is possible.

Admin commands:
- /addblocklist <blocklist trigger> <reason>: Add a blocklist trigger..
- /rmblocklist <blocklist trigger>: Remove a blocklist trigger.
- /unblocklistall: Remove all blocklist triggers - chat creator only.
- /blocklist: List all blocklisted items.
- /blocklistmode <blocklist mode>: Set the desired action to take when someone says a blocklisted item. Available: nothing/ban/mute/kick/warn/tban/tmute.
- /blocklistdelete <yes/no/on/off>: Set whether blocklisted messages should be deleted. Default: (on)
- /setblocklistreason <reason>: Set the default blocklist reason to warn people with.
- /resetblocklistreason: Reset the default blocklist reason to default - nothing.
"""
