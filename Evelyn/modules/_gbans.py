from datetime import datetime

from telethon import Button, events
from telethon.errors import ChatAdminRequiredError

from Evelyn import BOT_ID, OWNER_ID, tbot
from Evelyn.events import Cbot
from Evelyn.modules.sql.chats_sql import get_all_chat_id

from . import ELITES, SUDO_USERS, db, get_user

gbanned = db.gbanned


def get_reason(id):
    return gbanned.find_one({"user": id})


Ap_chat = int(-1001273171524)
Gban_logs = int(-1001466401634)

# Constants
main_text = """
<b>Originated From: {}<b\> <code>{}</code>
<b>Sudo Admin:</b> <a href="tg://user?id={}">{}</a>
<b>User:</b> <a href="tg://user?id={}">{}</a>
<b>ID:</b> <code>{}</code>
<b>Reason:</b> <i>{}</i>
<b>Event Stamp:</b> <code>{}</code>
"""
Ap_txt = (
    """
<b>[#]New Global Ban Request</b>"""
    + main_text
)

Ap_text = (
    """
<b>[#]New Global Ban</b>"""
    + main_text
)

Ap_update = (
    """
<b>[#]Global Ban Update</b>"""
    + main_text
)

up_update = (
    """
<b>[#]Global UnBan</b>"""
    + main_text
)
logs_text = """
<b>#GBANNED
Approved by <a href="tg://user?id={}">{}</a>

Requested to Gban by <a href="tg://user?id={}">{}</a></b>

<b>Banned User:</b> <a href="tg://user?id={}">{}</a>
<b>Banned User ID:</b> <code>{}</code>

<b>Reason:</b> <code>[EG-S] || requested to gban by {}</code>
<b>Chats affected:</b> 10
"""
gban_request = """
<b>#NEW GBAN REQUEST</b>

<b>Requested to Gban by <a href="tg://user?id={}">{}</a></b>

<b>User:</b> <a href="tg://user?id={}">{}</a>
<b>User ID:</b> <code>{}</code>

<b>Reason:</b> <code>{} || requested to gban by {}</code>
"""

ADMINS = SUDO_USERS + ELITES


@Cbot(pattern="^/testg ?(.*)")
async def gban(event):
    if not event.sender_id in ADMINS:
        return
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        return await event.reply(
            "You don't seem to be referring to a user or the ID specified is incorrect.."
        )
    user = None
    reason = None
    try:
        user, reason = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if user.id in ADMINS:
        return await event.reply("You can't ban bot admins.")
    if gbanned.find_one({"user": user.id}):
        await event.reply(
            "This user is already gbanned, I'm updating the reason of the gban with the new one"
        )
        return gbanned.find_one_and_update(
            {"user": user.id}, {"$set": {"reason": reason, "bannerid": event.sender_id}}
        )
    if event.sender_id in SUDO_USERS or ELITES:
        await event.reply("__Your request sent to DEVS waiting for approval. Till that send proofs to DEVS__.", buttons=Button.url("Send here", "t.me/Evelyn/support"))
        cb_data = str(event.sender_id) + "|" + str(user.id) + "|" + str(reason)
        buttons = [
            [Button.inline("Accept", data="gban_{}".format(cb_data))],
            [Button.inline("Decline", data="dec_gban")],
        ]
        text = gban_request.format(
            event.sender_id,
            event.sender.first_name,
            user.id,
            user.first_name,
            user.id,
            reason,
            event.sender_id,
        )
        await tbot.send_message(
            -1001273171524, text, buttons=buttons, parse_mode="html"
        )


@Cbot(pattern="^/gban ?(.*)")
async def _(event):
    if (
        not event.sender_id == OWNER_ID
        and not event.sender_id in ELITES
        and not event.sender_id in SUDO_USERS
    ):
        return
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        return await event.reply(
            "You don't seem to be referring to a user or the ID specified is incorrect.."
        )
    user, extra = await get_user(event)
    if extra:
        reason = extra
    else:
        reason = "None Given"
    if user.id == OWNER_ID:
        return await event.reply("Fool! You can't ban my master.🤣")
    elif user.id in ELITES:
        return await event.reply("Fool! You can't ban my dev.")
    elif user.id in SUDO_USERS:
        return await event.reply("Fool! You can't ban my sudo user🤨.")
    elif user.id == BOT_ID:
        return await event.reply("Kek, gbanning me...ಥ_ಥ")
    if not event.sender_id == OWNER_ID and not event.sender_id in ELITES:
        chats = gbanned.find({})
        for c in chats:
            if user.id == c["user"]:
                to_check = get_reason(id=user.id)
                gbanned.update_one(
                    {
                        "_id": to_check["_id"],
                        "bannerid": to_check["bannerid"],
                        "user": to_check["user"],
                        "reason": to_check["reason"],
                    },
                    {"$set": {"reason": reason, "bannerid": event.sender_id}},
                )
                await event.respond("the reason of the gban with the new one.")
                bote = [
                    Button.url("Appeal", "t.me/EvelynSupport"),
                    Button.url("Report", "t.me/EvelynSupport"),
                ]
                dtext = Ap_update.format(
                    event.chat.title,
                    event.chat_id,
                    event.sender_id,
                    event.sender.first_name,
                    user.id,
                    user.first_name,
                    user.id,
                    reason,
                    datetime.now(),
                )
                return await tbot.send_message(
                    Gban_logs, dtext, buttons=bote, parse_mode="htm"
                )
        buttons = Button.url("Send Here", "t.me/EvelynSupport")
        await event.reply(
            "__Your request sent to DEVS waiting for approval. Till that send proofs to DEVS.__",
            buttons=buttons,
        )
        cb_data = f"{event.chat.title}|{user.id}|{user.first_name[:15]}"
        bt = [
            Button.inline("Approve✅", data="agban_{}".format(cb_data)),
            Button.inline("Deny❌", data="deni"),
        ]
        dtext = Ap_txt.format(
            event.chat.title,
            event.chat_id,
            event.sender_id,
            event.sender.first_name,
            user.id,
            user.first_name,
            user.id,
            reason,
            datetime.now(),
        )
        await tbot.send_message(Ap_chat, dtext, buttons=bt, parse_mode="htm")
    else:
        chats = gbanned.find({})
        for c in chats:
            if user.id == c["user"]:
                to_check = get_reason(id=user.id)
                gbanned.update_one(
                    {
                        "_id": to_check["_id"],
                        "bannerid": to_check["bannerid"],
                        "user": to_check["user"],
                        "reason": to_check["reason"],
                    },
                    {"$set": {"reason": reason, "bannerid": event.sender_id}},
                )
                await event.respond(
                    "This user is already gbanned, I am updating the reason of the gban with your reason."
                )
                bote = [
                    Button.url("Appeal", "t.me/EvelynSupport"),
                    Button.url("Report", "t.me/EvelynSupport"),
                ]
                dtext = Ap_update.format(
                    event.chat.title,
                    event.chat_id,
                    event.sender_id,
                    event.sender.first_name,
                    user.id,
                    user.first_name,
                    user.id,
                    reason,
                    datetime.now(),
                )
                return await tbot.send_message(
                    Gban_logs, dtext, buttons=bote, parse_mode="htm"
                )
        await event.respond("**⚡Snaps the Banhammer⚡**")
        gbanned.insert_one(
            {"bannerid": event.sender_id, "user": user.id, "reason": reason}
        )
        dtext = Ap_text.format(
            event.chat.title,
            event.chat_id,
            event.sender_id,
            event.sender.first_name,
            user.id,
            user.first_name,
            user.id,
            reason,
            datetime.now(),
        )
        bote = [
            Button.url("Appeal", "t.me/EvelynSupport"),
            Button.url("Report", "t.me/EvelynSupport"),
        ]
        await tbot.send_message(Gban_logs, dtext, buttons=bote, parse_mode="htm")
        cats = get_all_chat_id()
        for i in cats:
            try:
                await tbot.edit_permissions(
                    int(i.chat_id), int(user.id), until_date=None, view_messages=False
                )
            except ChatAdminRequiredError:
                pass


@tbot.on(events.CallbackQuery(pattern=r"agban(\_(.*))"))
async def delete_fed(event):
    global box
    tata = event.pattern_match.group(1)
    data = tata.decode()
    if not event.sender_id == OWNER_ID and not event.sender_id in ELITES:
        return await event.answer("You need to be bot admin to do this.")
    user_id = data.split("_", 1)[1]
    title, user_id, first_name = user_id.split("|", 3)
    title = title.strip()
    user_id = int(user_id.strip())
    first_name = first_name.strip()
    await event.edit(
        event.text + "\n" + f"**Approved By {event.sender.first_name}**", buttons=None
    )
    final_txt = f"""
<b>[#]New GlobalBan</b>
<b>Originated From:</b> {title}
<b>Approved By:</b> <a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a>
<b>User:<b> <a href="tg://user?id={user_id}">{first_name}</a>
<b>ID:</b> <code>{user_id}</code>
<b>Event Stamp:</b> <code>{datetime.now()}</code>
"""
    buttons = [
        Button.url("Appeal", "t.me/EvelynSupport"),
        Button.url("Report", "t.me/EvelynSupport"),
    ]
    await tbot.send_message(Gban_logs, final_txt, buttons=buttons, parse_mode="html")
    gbanned.insert_one(
        {"bannerid": event.sender_id, "user": user_id, "reason": "Check Logs"}
    )
    cats = get_all_chat_id()
    for i in cats:
        try:
            await tbot.edit_permissions(
                int(i.chat_id), int(user_id), until_date=None, view_messages=False
            )
        except ChatAdminRequiredError:
            pass


@tbot.on(events.CallbackQuery(pattern="deni"))
async def lul(event):
    if not event.sender_id == OWNER_ID and not event.sender_id in ELITES:
        return await event.answer("You need to be bot admin to do this.")
    await event.edit(
        event.text + "\n" + f"Disapproved by **{event.sender.first_name}**.",
        buttons=None,
    )


@Cbot(pattern="^/ungban ?(.*)")
async def ungban(event):
    if (
        not event.sender_id == OWNER_ID
        and not event.sender_id in ELITES
        and not event.sender_id in SUDO_USERS
    ):
        return
    if not event.reply_to_msg_id and not event.pattern_match.group(1):
        return await event.reply(
            "You don't seem to be referring to a user or the ID specified is incorrect.."
        )
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if extra:
        reason = extra
    else:
        reason = "None Given"
    if user.id == OWNER_ID:
        return await event.reply("Fool,you can't ungban my master.🤭")
    elif user.id in ELITES:
        return await event.reply("Lmao u asking to ungban one of my devs.")
    elif user.id in SUDO_USERS:
        return await event.reply("Lmfao, that's a sudo user")
    elif user.id == BOT_ID:
        return await event.reply("Lol.")
    chats = gbanned.find({})
    for c in chats:
        if user.id == c["user"]:
            gbanned.delete_one({"user": user.id})
            await event.reply("Initialting regression of global ban.")
            txt = up_update.format(
                event.chat.title,
                event.chat_id,
                event.sender_id,
                event.sender.first_name,
                user.id,
                user.first_name,
                user.id,
                reason,
                datetime.now(),
            )
            return await tbot.send_message(Gban_logs, txt, parse_mode="html")
    await event.reply("This user is not globally banned.")
