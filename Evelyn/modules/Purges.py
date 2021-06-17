import asyncio

from telethon import Button, events, functions
from telethon.errors import UserAlreadyParticipantError
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.tl.functions.messages import ExportChatInviteRequest

from Jessica import BOT_ID, tbot, ubot
from Jessica.events import Cbot

from . import can_del_msg, db, is_owner

purgex = db.purge


def get_id(id):
    return purgex.find_one({"id": id})


@Cbot(pattern="^/purge ?(.*)")
async def pugre(event):
    if (
        event.text.startswith("!purgefrom")
        or event.text.startswith("/purgefrom")
        or event.text.startswith("?purgefrom")
        or event.text.startswith("!purgeto")
        or event.text.startswith("?purgeto")
        or event.text.startswith("/purgeto")
    ):
        return
    lt = event.pattern_match.group(1)
    if lt:
        if not lt.isdigit():
            lt = None
    if lt:
        limit = lt
    else:
        limit = 1000
    if event.is_group:
        if not await can_del_msg(event, event.sender_id):
            return
    if not event.reply_to_msg_id:
        return await event.reply("Reply to a message to show me where to purge from.")
    reply_msg = await event.get_reply_message()
    messages = []
    message_id = reply_msg.id
    delete_to = event.message.id
    messages.append(event.reply_to_msg_id)
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == limit:
            break
    try:
        await tbot.delete_messages(event.chat_id, messages)
    except MultiError:
        return await event.reply("I can't delete messages that are too old!")
    except MessageDeleteForbiddenError:
        return await event.reply("I can't delete messages that are too old!")
    x = await event.respond("Purge complete!")
    await asyncio.sleep(4)
    await x.delete()


@Cbot(pattern="^/purgefrom$")
async def lil(event):
    if event.is_group:
        if not await can_del_msg(event, event.sender_id):
            return
    if not event.reply_to_msg_id:
        return await event.reply("Reply to a message to let me know what to delete.")
    reply_msg = await event.get_reply_message()
    msg_id = reply_msg.id
    chats = purgex.find({})
    for c in chats:
        if event.chat_id == c["id"]:
            to_check = get_id(id=event.chat_id)
            purgex.update_one(
                {
                    "_id": to_check["_id"],
                    "id": to_check["id"],
                    "msg_id": to_check["msg_id"],
                },
                {"$set": {"msg_id": msg_id}},
            )
            return await event.respond(
                "Message marked for deletion. Reply to another message with /purgeto to delete all messages in between.",
                reply_to=msg_id,
            )
    purgex.insert_one({"id": event.chat_id, "msg_id": msg_id})
    await event.respond(
        "Message marked for deletion. Reply to another message with /purgeto to delete all messages in between.",
        reply_to=msg_id,
    )


@Cbot(pattern="^/purgeto$")
async def lilz(event):
    if event.is_group:
        if not await can_del_msg(event, event.sender_id):
            return
    if not event.reply_to_msg_id:
        return await event.reply("Reply to a message to let me know what to delete.")
    reply_msg = await event.get_reply_message()
    reply_msg.id
    msg_id = None
    chats = purgex.find({})
    for c in chats:
        if event.chat_id == c["id"]:
            msg_id = c["msg_id"]
    if msg_id == None:
        return await event.reply(
            "You can only use this command after having used the /purgefrom command."
        )
    messages = []
    limit = 1000
    delete_to = event.reply_to_msg_id
    messages.append(event.reply_to_msg_id)
    for id in range(msg_id, delete_to + 1):
        messages.append(id)
        if len(messages) == limit:
            break
    try:
        await tbot.delete_messages(event.chat_id, messages)
    except MessageDeleteForbiddenError:
        return await event.reply("I can't delete messages that are too old!")
    chats = purgex.find({})
    for c in chats:
        if event.chat_id == c["id"]:
            purgex.delete_one({"id": event.chat_id})


@Cbot(pattern="^/del")
async def deve(event):
    if event.from_id:
        if not await can_del_msg(event, event.sender_id):
            return
        if not event.reply_to:
            return await event.reply(
                "Reply to a message to let me know what to delete."
            )
        await (await event.get_reply_message()).delete()
        await event.delete()


@Cbot(pattern="^/spurge ?(.*)")
async def b(event):
    lt = event.pattern_match.group(1)
    if lt:
        if not lt.isdigit():
            lt = None
    if lt:
        limit = lt
    else:
        limit = 1000
    if event.is_group:
        if not await can_del_msg(event, event.sender_id):
            return
    if not event.reply_to_msg_id:
        return await event.reply("Reply to a message to show me where to purge from.")
    reply_msg = await event.get_reply_message()
    messages = []
    message_id = reply_msg.id
    delete_to = event.message.id
    messages.append(event.reply_to_msg_id)
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == limit:
            break
    try:
        await tbot.delete_messages(event.chat_id, messages)
    except MessageDeleteForbiddenError:
        return await event.reply("I can't delete messages that are too old!")


@Cbot(pattern="^/delall$")
async def kek(event):
    if event.is_private:
        return await event.reply("This command is made from groups and channels only.")
    elif event.is_group:
        if not await is_owner(event, event.sender_id):
            return
    buttons = [
        Button.inline("Delete All", data="d_all"),
        Button.inline("Cancel", data="d_a_cancel"),
    ]
    text = "Are you sure want to delete **ALL** messages of **{}**\n This can't be undone.".format(
        event.chat.title
    )
    await event.respond(text, buttons=buttons)


@tbot.on(events.CallbackQuery(pattern="d_all"))
async def ki(event):
    perm = await tbot.get_permissions(event.chat_id, event.sender_id)
    if not perm.is_admin:
        return await event.answer("You need to be an admin to do this.")
    if not perm.is_creator:
        return await event.answer("Chat creator required.")
    mp = await tbot.get_permissions(event.chat_id, BOT_ID)
    if not mp.add_admins:
        return await event.edit(
            "Unable to process delete **ALL** Process due to missing Permission: CanAddAdmins"
        )
    if not mp.delete_messages:
        return await event.edit(
            "Unable to process delete **ALL** Process due to missing Permission: CanDelMessages"
        )
    if not mp.invite_users:
        return await event.edit(
            "Unable to process delete **ALL** Process due to missing Permission: CanInviteUsers"
        )
    await event.edit("Begining the cleaning process....")
    try:
        link = await tbot(ExportChatInviteRequest(event.chat_id))
    except Exception as e:
        return await event.edit(str(e))
    link = (link.link).replace("https://t.me/joinchat/", "")
    try:
        result = await ubot(functions.messages.ImportChatInviteRequest(hash=link))
    except UserAlreadyParticipantError:
        pass
    except Exception as e:
        return await event.edit(str(e))
    await tbot.edit_admin(
        event.chat_id,
        1763477650,
        manage_call=False,
        add_admins=False,
        pin_messages=True,
        delete_messages=True,
        ban_users=True,
        change_info=True,
        invite_users=True,
        title="delall",
    )
    msg_id = event.id
    for msg_id in range(1, msg_id + 1):
        messages.append(msg_id)
        if len(messages) > 300:
            await ubot.delete_messages(event.chat_id, messages)
            messages = []
    await ubot.delete_messages(event.chat_id, messages)
    try:
        await tbot.kick_participant(event.chat_id, 1763477650)
    except:
        pass
    k = await event.edit("Cleaning Process Completed.")
    await asyncio.sleep(4)
    await k.delete()
