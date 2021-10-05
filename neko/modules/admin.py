import os

from telethon import Button
from telethon.errors.rpcerrorlist import (
    ChatAboutNotModifiedError,
    ChatNotModifiedError,
    ParticipantsTooFewError,
    UserAdminInvalidError,
)
from telethon.tl.functions.channels import (
    EditPhotoRequest,
    EditTitleRequest,
    SetStickersRequest,
)
from telethon.tl.functions.messages import EditChatAboutRequest, ExportChatInviteRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaDocument,
    MessageMediaPhoto,
    UserStatusLastMonth,
)

db = {}
from .. import CMD_HELP, OWNER_ID, tbot
from ..utils import Cbot, Cinline
from . import (
    DEVS,
    SUDO_USERS,
    can_change_info,
    can_promote_users,
    cb_can_promote_users,
    check_owner,
    get_user,
    is_admin,
    is_owner,
)

su = DEVS + SUDO_USERS
su.append(OWNER_ID)


@Cbot(pattern="^/promote(?: |$|@MissNeko_Bot)(.*)")
async def promote__user___(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in my PM!"
        )
    if not e.from_id:
        return await anonymous(e, "promote")
    if not e.sender_id in su:
        if not await can_change_info(e, e.sender_id):
            return
    user = None
    title = "Λ∂мιи"
    try:
        user, title = await get_user(e)
    except TypeError:
        pass
    if not user:
        return
    if e.sender_id == user.id:
        return await e.reply("Why are you trying to promote yourself?")
    try:
        await tbot.edit_admin(
            e.chat_id,
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
        name = "User"
        if user.first_name:
            name = user.first_name.replace("<", "&lt;").replace(">", "&gt!")
            if user.last_name:
                name = name + user.last_name
        await e.reply(
            f"Successfully promoted <b><a href='tg://user?id={user.id}'>{name}</a></b> !",
            parse_mode="html",
        )
    except:
        await e.reply(
            "I can't promote/demote people here!\nMake sure I'm admin and can appoint new admins."
        )


@Cbot(pattern="^/(superpromote|fullpromote)(?: |$|@MissNeko_Bot)(.*)")
async def super_promote(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in my PM!"
        )
    if not e.from_id:
        return await anonymous(e, "superpromote")
    if not e.sender_id in su:
        if not await can_promote_users(e, e.sender_id):
            return
    user = None
    title = "𝙎υρєя Λ∂мιи"
    try:
        user, title = await get_user(e)
    except TypeError:
        pass
    if not user:
        return
    try:
        await e.client.edit_admin(
            e.chat_id,
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
        name = user.first_name
        if name:
            name = (name.replace("<", "&lt;")).replace(">", "&gt!")
        await e.reply(
            f"Successfully promoted <a href='tg://user?id={user.id}'>{name}</a> with full rights!",
            parse_mode="html",
        )
    except UserAdminInvalidError:
        return await e.reply(
            "This user has already been promoted by someone other than me; I can't change their permissions!."
        )
    except:
        await e.reply("Seems like I don't have enough rights to do that.")


@Cbot(pattern="^/demote(?: |$|@MissNeko_Bot)(.*)")
async def _de(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in my PM!"
        )
    if not e.from_id:
        return await anonymous(e, "demote")
    if not e.sender_id in su:
        if not await can_promote_users(e, e.sender_id):
            return
    user = None
    try:
        user, title = await get_user(e)
    except TypeError:
        pass
    if not user:
        return
    if await check_owner(e, user.id):
        return await e.reply(
            "I don't really feel like staging a mutiny today, I think the chat owner deserves to stay an admin."
        )
    elif user.bot:
        return await e.reply(
            "Due to telegram limitations, I can't demote bots. Please demote them manually!"
        )
    if not await is_admin(e.chat_id, user.id):
        return await e.reply("This user isn't an admin anyway!")
    try:
        await e.client.edit_admin(
            e.chat_id,
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
        name = user.first_name
        if name:
            name = (name.replace("<", "&lt;")).replace(">", "&gt!")
        await e.reply(
            f"Demoted User <a href='tg://user?id={user.id}'>{name}</a> !",
            parse_mode="html",
        )
    except UserAdminInvalidError:
        return await e.reply(
            "This user was promoted by someone other than me; I can't change their permissions! Demote them manually."
        )
    except:
        await e.reply("Seems like I don't have enough rights to do that.")


async def a_ad(event, mode):
    user_id = None
    first_name = None
    e_t = None
    if event.reply_to:
        user = (await event.get_reply_message()).sender
        if isinstance(user, Channel):
            return
        user_id = user.id
        first_name = user.first_name
    elif event.pattern_match.group(1):
        u_obj = event.text.split(None, 2)[1]
        try:
            user = await tbot.get_entity(u_obj)
            user_id = user.id
            first_name = user.first_name
        except:
            pass
    try:
        if event.reply_to:
            e_t = event.text.split(None, 1)[1]
        elif user_id:
            e_t = event.text.split(None, 2)[2]
    except IndexError:
        e_t = None
    db[event.id] = [e_t, user_id, first_name]
    cb_data = str(event.id) + "|" + str(mode)
    a_buttons = Button.inline("Click to prove admin", data="bad_{}".format(cb_data))
    await event.reply(
        "It looks like you're anonymous. Tap this button to confirm your identity.",
        buttons=a_buttons,
    )


@Cinline(pattern=r"bad(\_(.*))")
async def _(e):
    d_ata = ((e.pattern_match.group(1)).decode()).split("_", 1)[1]
    da_ta = d_ata.split("|", 1)
    event_id = int(da_ta[0])
    try:
        cb_data = db[event_id]
    except KeyError:
        return await e.edit("This requests has been expired, please resend it.")
    user_id = cb_data[1]
    first_name = cb_data[2]
    title = cb_data[0]
    if not e.sender_id in su:
        if not await cb_can_promote_users(e, e.sender_id):
            return
    if mode == "promote":
        try:
            await e.client.edit_admin(
                e.chat_id,
                int(user_id),
                manage_call=False,
                add_admins=False,
                pin_messages=True,
                delete_messages=True,
                ban_users=True,
                change_info=True,
                invite_users=True,
                title=title if title else "Admin",
            )
            text = "Promoted <b><a href='tg://user?id={}'>{}</a> in <b>{}</b>.".format(
                user_id, first_name or "User", e.chat.title
            )
        except:
            text = "Seems like I don't have enough rights to do that."
    elif mode == "superpromote":
        try:
            await e.client.edit_admin(
                e.chat_id,
                int(user_id),
                manage_call=True,
                add_admins=True,
                pin_messages=True,
                delete_messages=True,
                ban_users=True,
                change_info=True,
                invite_users=True,
                title=title or "Admin",
            )
            text = "Promoted <b><a href='tg://user?id={}'>{}</a> in <b>{}</b> with full rights.".format(
                user_id, first_name or "User", e.chat.title
            )
        except:
            text = "Seems like I don't have enough rights to do that."
    elif mode == "demote":
        try:
            await e.client.edit_admin(
                e.chat_id,
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
            text = "Demoted <b><a href='tg://user?id={}'>{}</a> !".format(
                user_id, first_name or "User"
            )
        except:
            text = "Seems like I don't have enough rights to do that."
    await e.delete()
    await e.respond(text, parse_mode="html")


@Cbot(pattern="^/invitelink$")
async def link(event):
    if event.is_private:
        return  # connection
    if event.from_id:
        perm = await tbot.get_permissions(event.chat_id, event.sender_id)
        if not perm.is_admin:
            return await event.reply("You need to be an admin to do this ")
        if not perm.invite_users:
            return await event.reply(
                "You are missing the following rights to use this command: CanInviteUsers."
            )
    link = await tbot(ExportChatInviteRequest(event.chat_id))
    await event.reply(f"{link.link}", link_preview=False)


@Cbot(pattern="^/adminlist$")
async def admeene(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.chat.admin_rights.ban_users:
        return
    mentions = f"Admins in **{event.chat.title}:**"
    async for user in tbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        if not user.bot:
            if not user.deleted:
                if user.username:
                    link = "- @{}".format(user.username)
                    mentions += f"\n{link}"
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
    async for c in tbot.iter_participants(event.chat_id):
        if isinstance(c.status, UserStatusLastMonth):
            try:
                await tbot.kick_participant(event.chat_id, c.id)
                total += 1
            except:
                pass
    if total == 0:
        return await zec.edit("congo, No inactive users to kick.")
    await zec.edit(f"Sucessfully kicked {total} Inactive users.")


@Cbot(pattern="^/bots$")
async def bot(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if event.is_group:
        if not await is_admin(event.chat_id, event.sender_id):
            return await event.reply("Only admins can execute this command!")
    final = f"Bots in __{event.chat.title}__:"
    async for user in tbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsBots
    ):
        final += f"\n- @{user.username}"
    await event.reply(final)


@Cbot(pattern="^/rpromote(?: |$|@MissNeko_Bot)(.*)")
async def kek(event):
    if not event.sender_id == OWNER_ID:
        return
    user = None
    try:
        user, chat = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if chat:
        if chat.replace("-", "").isnumeric():
            chat = int(chat)
    try:
        chat = await tbot.get_entity(chat)
    except (TypeError, ValueError):
        return await event.reply("Unable to find the chat/channel!")
    chat_id = chat.id
    try:
        await tbot.edit_admin(
            chat_id,
            int(user_id),
            manage_call=True,
            add_admins=True,
            pin_messages=True,
            delete_messages=True,
            ban_users=True,
            change_info=True,
            invite_users=True,
            title="NK Admin",
        )
        await event.reply(f"Promoted **{user.first_name}** in **{chat.title}**")
    except:
        await event.reply("Seems like I don't have enough rights to do that.")


@Cbot(pattern="^/setgpic$")
async def x_pic(e):
    if not e.is_channel:
        return await e.reply("This command is made to be used in groups!")
    if e.from_id:
        if not await can_change_info(e, e.sender_id):
            return
    if not e.reply_to:
        return await e.reply("Reply to some photo or file to set new chat pic!")
    reply = await e.get_reply_message()
    if e.chat.admin_rights:
        if not e.chat.admin_rights.change_info:
            return await e.reply("Error! Not enough rights to change chat photo")
    else:
        return
    if not reply.media:
        return await e.reply("That's not a valid image for group pic!")
    elif isinstance(reply.media, MessageMediaPhoto):
        photo = reply.media.photo
    elif (
        isinstance(reply.media, MessageMediaDocument)
        and reply.media.document.mime_type.split("/", 1)[0] == "image"
    ):
        photo = reply.media.document
        photo_x = await tbot.download_media(photo, "photo.jpg")
        photo = await tbot.upload_file(photo_x)
        os.remove(photo_x)
    else:
        return await e.reply("That's not a valid image for group photo!")
    try:
        await tbot(EditPhotoRequest(e.chat_id, photo))
    except Exception as x:
        return await e.reply(str(x))
    await e.reply("✨ Successfully set new chatpic!")


@Cbot(pattern="^/setgtitle(?: |$|@MissNeko_Bot)(.*)")
async def x_title(e):
    if not e.is_group:
        return await e.reply("This command is made to be used in groups!")
    if e.from_id:
        if not await can_change_info(e, e.sender_id):
            return
    if not e.pattern_match.group(1):
        return await e.reply("Enter some text to set new title in your chat!")
    if e.chat.admin_rights:
        if not e.chat.admin_rights.change_info:
            return await e.reply("Error! Not enough rights to change chat title")
    else:
        return
    text = e.pattern_match.group(1)
    try:
        await tbot(EditTitleRequest(e.chat_id, text))
        await e.reply(f"✨ Successfully set **{text}** as new chat title!")
    except ChatNotModifiedError:
        await e.reply(f"✨ Successfully set **{text}** as new chat title!")
    except Exception as x:
        await e.reply(str(x))


@Cbot(pattern="^/setgsticker$")
async def x_sticker_set(e):
    if not e.is_channel:
        return await e.reply("This command is made to be used in groups!")
    if e.from_id:
        if not await can_change_info(e, e.sender_id):
            return
    if not e.reply_to:
        return await e.reply("Reply to some sticker to set new chat sticker pack!")
    reply = await e.get_reply_message()
    if not reply.media:
        return await e.reply(
            "You need to reply to some sticker to set chat sticker set!"
        )
    if not isinstance(reply.media, MessageMediaDocument):
        return await e.reply(
            "You need to reply to some sticker to set chat sticker set!"
        )
    x_meme = reply.media.document.mime_type
    if not str(x_meme) == "image/webp":
        return await e.reply(
            "You need to reply to some sticker to set chat sticker set!"
        )
    sticker_set_id = sticker_set_access_hash = None
    try:
        for x in range(len(reply.media.document.attributes)):
            _x = reply.media.document.attributes[x]
            if isinstance(_x, DocumentAttributeSticker):
                sticker_set_id = _x.stickerset.id
                sticker_set_access_hash = _x.stickerset.access_hash
    except Exception as x:
        return await e.reply(
            "You need to reply to some sticker to set chat sticker set!" + str(x)
        )
    if not sticker_set_id:
        return await e.reply("Failed to find the sticker set for the sticker!")
    try:
        await tbot(
            SetStickersRequest(
                e.chat_id,
                InputStickerSetID(
                    id=sticker_set_id, access_hash=sticker_set_access_hash
                ),
            )
        )
        await e.reply(f"✨ Successfully set new group stickers in {e.chat.title}!")
    except ChatNotModifiedError:
        await e.reply(f"✨ Successfully set new group stickers in {e.chat.title}!")
    except ParticipantsTooFewError:
        await e.reply("Failed to set stickerset, Not enough participants.")
    except Exception as x:
        await e.reply(str(x))


@Cbot(pattern="^/(setgdesc|setgdescription)(?: |$|@MissNeko_Bot)(.*)")
async def x_description(e):
    if not e.is_channel:
        return await e.reply("This command is made to be used in groups!")
    if e.from_id:
        if not await can_change_info(e, e.sender_id):
            return
    if not e.reply_to:
        try:
            about = e.text.split(None, 1)[1]
        except IndexError:
            about = ""
        if not about:
            await e.reply(f"✨ Sucessfully removed chat description in {e.chat.title}")
    elif e.reply_to:
        reply = await e.get_reply_message()
        if not reply.text:
            await e.reply(f"✨ Sucessfully removed chat description in {e.chat.title}")
        about = reply.text or ""
    try:
        await tbot(EditChatAboutRequest(e.chat_id, about))
        if not about == "":
            await e.reply(f"✨ Successfully updated chat description in {e.chat.title}!")
    except ChatAboutNotModifiedError:
        if not about == "":
            await e.reply(f"✨ Successfully updated chat description in {e.chat.title}!")
    except Exception as x:
        await e.reply(str(x))


__name__ = "admin"
__help__ = """
Help menu for the **Admin** module:

**Admin Commands:**
- /promote `<user> <rank>`: Promote a user.
- /superpromote &&
- /fullpromote `<user> <rank>`: Promote a user with full rights.
- /demote `<user>`: Demote a user.

- /setgtitle `<title>`: Edit the group title.
- /setgpic `<reply to image>`: Set the group Profile Photo.
- /setgdesc `<text>`: Edit the group description.
- /setgsticker `<reply to sticker>`: Set the group sticker pack.

- /adminlist: List the admins of the chat.
- /bots: List all the bots of the chat.
- /kickthefools: Kick participants who were inactive for over a month.
- /invitelink: Export the chat Invite Link.
"""
CMD_HELP.update({__name__: [__name__, __help__]})
