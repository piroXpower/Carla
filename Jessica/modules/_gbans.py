from telethon import Button, events

from Jessica import OWNER_ID, tbot
from Jessica.events import Cbot
from Jessica.modules.sql.chats_sql import get_all_chat_id

from . import DEVS, ELITES, SUDO_USERS, db, get_user

gbanned = db.gbanned

logs_text = """
<b>#GBANNED
Originated From: <a href="t.me/{}">{}</a>
Sudo Admin: <a href="tg://user?id={}">{}</a></b>

<b>Banned User:</b> <a href="tg://user?id={}">{}</a>
<b>Banned User ID:</b> <code>{}</code>

<b>Reason:</b> <code>{} || gbanned by {}</code>
<b>Chats affected:</b> {}
"""
logs_approved_text = """
<b>#GBANNED
Approved by <a href="tg://user?id={}">{}</a>

Requested to Gban by <a href="tg://user?id={}">{}</a></b>

<b>Banned User:</b> <a href="tg://user?id={}">{}</a>
<b>Banned User ID:</b> <code>{}</code>

<b>Reason:</b> <code>{} || requested to gban by {}</code>
<b>Chats affected:</b> {}
"""
rejected_req = """
<b>#REJECTED</b>
<b>Rejected by <a href="tg://user?id={}">{}</a></b>

<b>Requested to Gban by <a href="tg://user?id={}">{}</a></b>

<b>User:</b> <a href="tg://user?id={}">{}</a>
<b>User ID:</b> <code>{}</code>

<b>Reason:</b> <code>{} || requested to gban by {}</code>
"""
approved_req = """
<b>#APPROVED</b>
<b>Approved by <a href="tg://user?id={}">{}</a></b>

<b>Requested to Gban by <a href="tg://user?id={}">{}</a></b>

<b>User:</b> <a href="tg://user?id={}">{}</a>
<b>User ID:</b> <code>{}</code>

<b>Reason:</b> <code>{} || requested to gban by {}</code>
"""
gban_request = """
<b>#NEW_GBAN_REQUEST</b>

<b>Requested to Gban by <a href="tg://user?id={}">{}</a></b>

<b>User:</b> <a href="tg://user?id={}">{}</a>
<b>User ID:</b> <code>{}</code>

<b>Reason:</b> <code>{} || requested to gban by {}</code>
"""
un_gban_req = """
<b>#UNGBAN
Sudo Admin: <a href="tg://user?id={}">{}</a></b>

<b>Unbanned User:</b> <a href="tg://user?id={}">{}</a>
<b>Unbanned User ID:</b> <code>{}</code>

<b>Reason:</b> <code>{} || gbanned by {}</code>
"""
gbanned_acc = """
<b>#Alert</b>
<i>GBANNED User detected, banned.</i>
<b>User:</b> <a href="tg://user?id={}">{}</a> (<code>{}</code>)
<b>Appeal: @JessicaSupport</b>
"""

ADMINS = SUDO_USERS + ELITES

CODES = {
    "NC-1": "[NC-1] - Sᴄᴀᴍᴍᴇʀ",
    "NC-2": "[NC-2] - Mᴇᴍʙᴇʀs Sᴄʀᴀᴘᴘᴇʀ / Aᴅᴅɪɴɢ Sᴘᴀᴍ Bᴏᴛs",
    "NC-3": "[NC-3] - Sᴘᴀᴍᴍᴇʀ / Nsғᴡ Sᴘᴀᴍᴍᴇʀ",
    "NC-4": "[NC-4] - Lɪᴄᴇɴsᴇ Vɪᴏʟᴀᴛɪᴏɴs",
    "NC-5": "[NC-5] - Bᴛᴄ Sᴄᴀᴍ",
    "NC-6": "[NC-6] - Aᴅᴍɪɴ Rɪɢʜᴛs Aʙᴜsᴇ",
    "NC-7": "[NC-7] - Fʀᴀᴜᴅ Pʀᴏᴍᴏᴛɪᴏɴ",
    "NC-8": "[NC-8] - Rᴀɪᴅ Iɴɪᴛɪᴀʟɪᴢᴏʀ / Pᴀʀᴛɪᴄɪᴘᴀɴᴛ",
    "NC-9": "[NC-9] - Mғ Aʀᴀʙ Nsғᴡ Bᴏᴛs",
    "NC-N": "[NC-N] - Nᴏ Rᴇᴀsᴏɴ (Wᴏɴᴛ Bᴇ Aᴄᴄᴇᴘᴛᴇᴅ)",
}


@Cbot(pattern="^/gban ?(.*)")
async def gban(event):
    if not event.sender_id in SUDO_USERS and not event.sender_id in DEVS and not event.sender_id == OWNER_ID:
        return
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        return await event.reply(
            "You don't seem to be referring to a user or the ID specified is incorrect.."
        )
    user = None
    reason = None
    cb_reason = "[NC-N]"
    try:
        user, reason = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if reason:
        cb_reason = reason[:6]
    if user.id in SUDO_USERS:
        return await event.reply(
            "This is one of my sudo users, you can't act against them!"
        )
    elif user.id == OWNER_ID:
        return await event.reply("fuck off bitch, how dare you try to ban my master🤨.")
    elif user.id in DEVS:
        return await event.reply(
            "This is one of my dev users, you can't act against them!"
        )
    if gbanned.find_one({"user": user.id}):
        await event.reply(
            "This user is already gbanned, I'm updating the reason of the gban with the new one"
        )
        return gbanned.find_one_and_update(
            {"user": user.id}, {"$set": {"reason": reason, "bannerid": event.sender_id}}
        )
    if event.sender_id in SUDO_USERS:
        await event.reply(
            "__Your request sent to DEVS waiting for approval. Till that send proofs to DEVS__.",
            buttons=Button.url("Send here", "t.me/RxturnZbot"),
        )
        cb_data = str(event.sender_id) + "|" + str(user.id) + "|" + str(cb_reason)
        buttons = [
            [Button.inline("Accept", data="gban_{}".format(cb_data))],
            [Button.inline("Decline", data="rgban_{}".format(cb_data))],
        ]
        text = gban_request.format(
            event.sender_id,
            event.sender.first_name,
            user.id,
            user.first_name,
            user.id,
            cb_reason,
            event.sender_id,
        )
        await tbot.send_message(
            -1001463516878, text, buttons=buttons, parse_mode="html"
        )
    elif event.sender_id in DEVS or event.sender_id == OWNER_ID:
        await event.reply("⚡Snaps the banhammer⚡")
        gbanned.insert_one(
            {"bannerid": event.sender_id, "user": user.id, "reason": reason}
        )
        buttons = [
            [
                Button.url("Appeal", "https://t.me/NekoChan_Support"),
                Button.url("Proofs", "https://t.me/NekoChan_Support"),
            ],
            [
                Button.url(
                    "Fban in your fed",
                    f"https://t.me/share/text?text=/fban%20{user.id}%20{cb_reason}%20Appeal%20Chat%20@NekoChan_Support",
                )
            ],
        ]

        all_chats = get_all_chat_id()
        gbanned_chats = 0
        for chat in all_chats:
            try:
                await tbot.edit_permissions(
                    int(chat.chat_id), user.id, view_messages=False
                )
                gbanned_chats += 1
            except:
                pass
        g_text = logs_text.format(
            event.chat.username,
            event.chat.title,
            event.sender_id,
            event.sender.first_name,
            user.id,
            user.first_name,
            user.id,
            cb_reason,
            event.sender_id,
            gbanned_chats,
        )
        await tbot.send_message(
            -1001504249078,
            g_text,
            parse_mode="html",
            buttons=buttons,
            link_preview=False,
        )


@tbot.on(events.CallbackQuery(pattern=r"gban(\_(.*))"))
async def cb_gban(event):
    if not event.sender_id == OWNER_ID and not event.sender_id in DEVS:
        return await event.answer("You don't have access to use this!", alert=True)
    cb_data = (((event.pattern_match.group(1)).decode()).split("_")[1]).split("|", 3)
    banner_id = int(cb_data[0])
    user_id = int(cb_data[1])
    cb_reason = cb_data[2]
    try:
        banner = await tbot.get_entity(banner_id)
        user = await tbot.get_entity(user_id)
    except:
        return await event.edit("Request expired!", buttons=None)
    final_text = approved_req.format(
        event.sender_id,
        event.sender.first_name,
        banner.id,
        banner.first_name,
        user.id,
        user.first_name,
        user.id,
        cb_reason,
        banner.id,
    )
    await event.edit(final_text, buttons=None, parse_mode="html")
    gbanned.insert_one({"bannerid": banner.id, "user": user.id, "reason": cb_reason})
    all_chats = get_all_chat_id()
    gbanned_chats = 0
    for chat in all_chats:
        try:
            await tbot.edit_permissions(int(chat.chat_id), user.id, view_messages=False)
            gbanned_chats += 1
        except:
            pass
    buttons = [
        [
            Button.url("Appeal", "t.me/NekoChan_Support"),
            Button.url("Proofs", "t.me/NekoChan_Support"),
        ],
        [
            Button.url(
                "Fban in your fed",
                f"https://t.me/share/text?text=/fban%20{user.id}%20{cb_reason}%20Appeal%20Chat%20@Jessicasupport",
            )
        ],
    ]
    logs_send = logs_approved_text.format(
        event.sender_id,
        event.sender.first_name,
        banner.id,
        banner.first_name,
        user.id,
        user.first_name,
        user.id,
        cb_reason,
        banner.id,
        gbanned_chats,
    )
    await tbot.send_message(
        -1001504249078, logs_send, buttons=buttons, parse_mode="html"
    )


@tbot.on(events.CallbackQuery(pattern=r"rgban(\_(.*))"))
async def cb_gban(event):
    if not event.sender_id == OWNER_ID and not event.sender_id in DEVS:
        return await event.answer("You don't have access to use this!", alert=True)
    cb_data = (((event.pattern_match.group(1)).decode()).split("_")[1]).split("|", 3)
    banner_id = int(cb_data[0])
    user_id = int(cb_data[1])
    cb_reason = cb_data[2]
    try:
        banner = await tbot.get_entity(banner_id)
        user = await tbot.get_entity(user_id)
    except:
        return await event.edit("Request expired!", buttons=None)
    final_text = rejected_req.format(
        event.sender_id,
        event.sender.first_name,
        banner.id,
        banner.first_name,
        user.id,
        user.first_name,
        user.id,
        cb_reason,
        banner.id,
    )
    await event.edit(final_text, buttons=None, parse_mode="html")


@Cbot(pattern="^/ungban ?(.*)")
async def ungban(event):
    if (
        not event.sender_id in DEVS
        and not event.sender_id in SUDO_USERS
        and not event.sender_id == OWNER_ID
    ):
        return
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        return await event.reply(
            "You don't seem to be referring to a user or the ID specified is incorrect.."
        )
    user = None
    reason = None
    cb_reason = "[NC-N]"
    try:
        user, reason = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if reason:
        cb_reason = reason[:6]
    if user.id in ADMINS:
        return await event.reply("I'm sorry, but you can't unban other bot admins.")
    check = gbanned.find_one({"user": user.id})
    if check:
        banner_id = check["bannerid"]
        await event.reply(
            f"Initiating Regression of global ban on <b><a href='tg://user?id={user.id}'>{user.first_name}</a></b>",
            parse_mode="html",
        )
        gbanned.delete_one({"user": user.id})
        buttons = [
            [
                Button.url("Appeal", "https://t.me/NekoChan_Support"),
            ],
            [
                Button.url(
                    "UnFban in your fed",
                    f"https://t.me/share/text?text=/unfban%20{user.id}%20Appeal%20Chat%20@NekoChan_Support",
                )
            ],
        ]
        logs_text = un_gban_req.format(
            event.sender_id,
            event.sender.first_name,
            user.id,
            user.first_name,
            user.id,
            cb_reason,
            banner_id,
        )
        await tbot.send_message(
            -1001504249078, logs_text, parse_mode="html", buttons=buttons
        )
    else:
        await event.reply("This user is not gbanned!")


@tbot.on(events.NewMessage())
async def gban_check(event):
    if not event.is_group:
        return
    if gbanned.find_one({"user": event.sender_id}):
        if event.chat.admin_rights:
            if event.chat.admin_rights.ban_users:
                try:
                    await tbot.edit_permissions(
                        event.chat_id, event.sender_id, view_messages=False
                    )
                except:
                    return
                await event.reply(
                    gbanned_acc.format(
                        event.sender_id, event.sender.first_name, event.sender_id
                    ),
                    parse_mode="html",
                )


@tbot.on(events.ChatAction())
async def gban_check(event):
    if not event.is_group:
        return
    if event.user_joined:
        if gbanned.find_one({"user": event.user_id}):
            if event.chat.admin_rights:
                if event.chat.admin_rights.ban_users:
                    await event.reply(
                        gbanned_acc.format(
                            event.user_id, event.user.first_name, event.user_id
                        ),
                        parse_mode="html",
                    )
                    await tbot.edit_permissions(
                        event.chat_id, event.user_id, view_messages=False
                    )
