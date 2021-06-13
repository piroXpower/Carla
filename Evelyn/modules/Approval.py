from Evelyn.events import Cbot

from . import can_ban_users, db, get_user, is_admin

approve_d = db.approved


@Cbot(pattern="^/approve ?(.*)")
async def appr(event):
    if (
        event.text.startswith(".approved")
        or event.text.startswith("/approved")
        or event.text.startswith("!approved")
        or event.text.startswith("?approved")
        or event.text.startswith("?approval")
        or event.text.startswith(".approval")
        or event.text.startswith("/approval")
        or event.text.startswith("!approved")
    ):
        return
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if not await can_ban_users(event, event.sender_id):
            return
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if await is_admin(event.chat_id, user.id):
            return await event.reply(
                "User is already admin - locks, blocklists, and antiflood already don't apply to them."
            )
        a_str = "<a href='tg://user?id={}'>{}</a> has been approved in {}! They will now be ignored by automated admin actions like locks, blocklists, and antiflood."
        await event.respond(
            a_str.format(user.id, user.first_name, event.chat.title),
            reply_to=event.reply_to_msg_id or event.id,
            parse_mode="html",
        )
        if not approve_d.find_one({"user_id": user.id, "chat_id": event.chat_id}):
            approve_d.insert_one({"user_id": user.id, "chat_id": event.chat_id})


@Cbot(pattern="^/disapprove ?(.*)")
async def dissapprove(event):
    if (
        event.text.startswith(".disapproveall")
        or event.text.startswith("!disapproveall")
        or event.text.startswith("?disapproveall")
        or event.text.startswith("/disapproveall")
    ):
        return
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if not await can_ban_users(event, event.sender_id):
            return
        user = None
        try:
            user, reason = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if await is_admin(event.chat_id, user.id):
            return await event.reply("This user is an admin, they can't be unapproved.")
        if approved.find_one({"user_id": user.id, "chat_id": event.chat_id}):
            await event.reply(
                f"{user.first_name} is no longer approved in {event.chat.title}."
            )
            return approve_d.delete_one({"user_id": user.id})
        await event.reply(f"{user.first_name} isn't approved yet!")


@Cbot(pattern="^/approved")
async def approved(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.from_id:
        if not await can_ban_users(event, event.sender_id):
            return
