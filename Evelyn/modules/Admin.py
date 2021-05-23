from telethon import Button, events
from telethon.tl.functions.messages import ExportChatInviteRequest

from Evelyn import BOT_ID, OWNER_ID, tbot
from Evelyn.events import Cbot

from . import ELITES, can_promote_users, cb_can_promote_users, get_user, is_admin

btext = "It looks like you're anonymous. Tap this button to confirm your identity."


@Cbot(pattern="^/promote ?(.*)")
async def _(event):
    if event.is_private:
        return  # connection
    title = None
    if event.from_id:
        if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
            if not await can_promote_users(event, event.sender_id):
                return
        try:
            user, title = await get_user(event)
        except:
            pass
        if not user:
            return
        if not title:
            title = "Admin"
        if await is_admin(event.chat_id, user.id):
            return await event.reply("This User is already an Admin!")
        try:
            await tbot.edit_admin(
                event.chat_id,
                user.id,
                manage_call=False,
                add_admins=False,
                pin_messages=True,
                delete_messages=True,
                ban_users=True,
                change_info=True,
                invite_users=True,
                title=title,
            )
            await event.reply(
                f"Promoted **{user.first_name}** in **{event.chat.title}**."
            )
        except:
            await event.reply("Seems like I don't have enough rights to do that.")
    else:
        await anonymous(event, "promote")


@Cbot(pattern="^/superpromote ?(.*)")
async def _(event):
    if event.is_private:
        return  # connection
    title = None
    if event.from_id:
        if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
            k = await can_promote_users(event, event.sender_id)
            if not k:
                return
        try:
            user, title = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if not title:
            title = "Admin"
        if await is_admin(event.chat_id, user.id):
            return await event.reply("This User is already an Admin!")
        try:
            await tbot.edit_admin(
                event.chat_id,
                user.id,
                manage_call=True,
                add_admins=True,
                pin_messages=True,
                delete_messages=True,
                ban_users=True,
                change_info=True,
                invite_users=True,
                title=title,
            )
            await event.reply(
                f"Promoted **{user.first_name}** in **{event.chat.title}** with full Rights."
            )
        except:
            await event.reply("Seems like I don't have enough rights to do that.")
    else:
        await anonymous(event, "superpromote")


@Cbot(pattern="^/demote ?(.*)")
async def _(event):
    if event.is_private:
        return  # connection
    if event.from_id:
        if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
            k = await can_promote_users(event, event.sender_id)
            if not k:
                return
        try:
            user, title = await get_user(event)
        except TypeError:
            pass
        if not user:
            return
        if user.bot:
            return await event.reply(
                "Due to telegram limitations, I can't demote bots. Please demote them manually!"
            )
        if not await is_admin(event.chat_id, user.id):
            return await event.reply("This User is not an Admin!")
        try:
            await tbot.edit_admin(
                event.chat_id,
                user.id,
                is_admin=False,
                manage_call=False,
                add_admins=False,
                pin_messages=False,
                delete_messages=False,
                ban_users=False,
                change_info=False,
                invite_users=False,
            )
            await event.reply(f"Demoted **{user.first_name}**.")
        except:
            await event.reply("Seems like I don't have enough rights to do that.")
    else:
        await anonymous(event, "demote")


async def anonymous(event, mode):
    try:
        user, title = await get_user(event)
    except:
        pass
    if not user:
        return
    if user.bot and mode == "demote":
        return await event.reply(
            "Due to telegram limitations, I can't demote bots. Please demote them manually!"
        )
    data = f"{user.id}!{mode}"
    buttons = Button.inline("Click to prove Admin", data="sup_{}".format(data))
    await event.reply(btext, buttons=buttons)


@tbot.on(events.CallbackQuery(pattern=r"sup(\_(.*))"))
async def _(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    input = data.split("_", 1)[1]
    user_id, mode = input.split("!", 1)
    user_id = user_id.strip()
    mode = mode.strip()
    if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
        k = await cb_can_promote_users(event, event.sender_id)
        if not k:
            return
    if mode == "promote":
        try:
            await tbot.edit_admin(
                event.chat_id,
                int(user_id),
                manage_call=False,
                add_admins=False,
                pin_messages=True,
                delete_messages=True,
                ban_users=True,
                change_info=True,
                invite_users=True,
                title="Admin",
            )
            text = f"Promoted **User** in **{event.chat.title}**."
        except:
            text = "Seems like I don't have enough rights to do that."
    elif mode == "superpromote":
        try:
            await tbot.edit_admin(
                event.chat_id,
                int(user_id),
                manage_call=True,
                add_admins=True,
                pin_messages=True,
                delete_messages=True,
                ban_users=True,
                change_info=True,
                invite_users=True,
                title="Admin",
            )
            text = f"Promoted **User** in **{event.chat.title}** with full Rights."
        except:
            text = "Seems like I don't have enough rights to do that."
    elif mode == "demote":
        try:
            await tbot.edit_admin(
                event.chat_id,
                int(user_id),
                is_admin=False,
                manage_call=False,
                add_admins=False,
                pin_messages=False,
                delete_messages=False,
                ban_users=False,
                change_info=False,
                invite_users=False,
            )
            text = "Demoted!."
        except:
            text = "Seems like I don't have enough rights to do that."
    await event.edit(text)


@Cbot(pattern="^/invitelink")
async def link(event):
    if event.is_private:
        return  # connection
    if event.from_id:
        if not await is_admin(event.chat_id, event.sender_id):
            return await event.reply("You need to be an admin to do this ")
        perm = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not perm.invite_users:
            return await event.reply(
                "You are missing the following rights to use this command: CanInviteUsers."
            )
        link = await tbot(ExportChatInviteRequest(event.chat_id))
        await event.reply(f"`{link.link}`", link_preview=False)
    else:
        link = await tbot(ExportChatInviteRequest(event.chat_id))
        await event.reply(f"`{link.link}`", link_preview=False)


@Cbot(pattern="^/adminlist")
async def admeene(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not await is_admin(event.chat_id, BOT_ID):
        return
    mentions = f"Admins in **{event.chat.title}:**"
    async for user in tbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        if not user.bot:
            if not user.deleted:
                if user.username:
                    link_unf = "- @{}"
                    link = link_unf.format(user.username)
                    mentions += f"\n{link}"
    mentions += "\n\nNote: These values are up-to-date"
    await event.reply(mentions)

@Cbot(pattern="^/kickthefools$")
async def kekthem(event):
  if event.is_private:
    return await event.reply("This command is made for Groups, not my PM.")
  if not await is_owner(event, event.sender_id):
    return
  if not event.chat.admin_rights.ban_users:
    return await event.reply("Unable to perform, not enough rights.")
  total = 0
  zec = await event.reply("Working....")
  async for user in iter_participants(event.chat_id):
    if str(user.status) == "UserStatusLastMonth()":
       await tbot.kick_participant(event.chat_id, user.id)
       total += 1
  if total == 0:
       return await zec.edit("No inactive users to kick.")
  await zec.edit("Sucessfully kicked {total} Inactive users.")
