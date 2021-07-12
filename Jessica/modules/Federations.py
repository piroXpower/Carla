import time
import uuid

from telethon import Button

import Jessica.modules.mongodb.feds_db as db
import Jessica.modules.sql.feds_sql as sql
from Jessica import BOT_ID, OWNER_ID
from Jessica.events import Cbot, Cinline

from . import ELITES, SUDO_USERS, get_user, is_admin, is_owner

# im_bannable
ADMINS = ELITES + SUDO_USERS
ADMINS.append(BOT_ID)
p_reason = ""


def is_user_fed_admin(fed_id, user_id):
    fed_admins = db.get_all_fed_admins(fed_id)
    if int(user_id) in fed_admins or int(user_id) == OWNER_ID:
        return True
    else:
        return False


def is_user_fed_owner(fed_id, user_id):
    getsql = sql.get_fed_info(fed_id)
    if getsql is False:
        return False
    getfedowner = eval(getsql["fusers"])
    if getfedowner is None or getfedowner is False:
        return False
    getfedowner = getfedowner["owner"]
    if str(user_id) == getfedowner or int(user_id) == OWNER_ID:
        return True
    else:
        return False


@Cbot(pattern="^/newfed ?(.*)")
async def newfed(event):
    if not event.is_private:
        return await event.reply("Create your federation in my PM - not in a group.")
    name = event.pattern_match.group(1)
    f_owner = db.get_user_owner_fed_full(event.sender_id)
    if f_owner:
        fed_name = f_owner[1]
        return await event.reply(
            f"You already have a federation called `{fed_name}` ; you can't create another. If you would like to rename it, use `/renamefed`."
        )
    if not name:
        return await event.reply(
            "You need to give your federation a name! Federation names can be up to 64 characters long."
        )
    if len(name) > 64:
        return await event.reply(
            "Federation names can only be upto 64 charactors long."
        )
    fed_id = str(uuid.uuid4())
    db.new_fed(event.sender_id, fed_id, name)
    await event.reply(
        f"Created new federation with FedID: `{fed_id}`.\nUse this ID to join the federation! eg:\n`/joinfed {fed_id}`"
    )


@Cbot(pattern="^/delfed")
async def del_fed(event):
    if not event.is_private:
        return await event.reply("Delete your federation in my PM - not in a group.")
    fedowner = db.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply("It doesn't look like you have a federation yet!")
    name = fedowner[1]
    fed_id = fedowner[0]
    await event.respond(
        "Are you sure you want to delete your federation? This action cannot be undone - you will lose your entire ban list, and '{}' will be permanently gone.".format(
            name
        ),
        buttons=[
            [Button.inline("Delete Federation", data="rmfed_{}".format(fed_id))],
            [Button.inline("Cancel", data="cancel_delete")],
        ],
    )


@Cinline(pattern=r"rmfed(\_(.*))")
async def delete_fed(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    fed_id = data.split("_", 1)[1]
    db.del_fed(fed_id)
    await event.edit(
        "You have deleted your federation! All chats linked to it are now federation-less."
    )


@Cinline(pattern=r"cancel_delete")
async def delete_fed(event):
    await event.edit("Federation deletion cancelled.")


@Cbot(pattern="^/renamefed ?(.*)")
async def rename(event):
    if not event.is_private:
        return await event.reply("You can only rename your fed in PM.")
    fedowner = db.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply("It doesn't look like you have a federation yet!")
    if not event.pattern_match.group(1):
        return await event.reply(
            "You need to give your federation a new name! Federation names can be up to 64 characters long."
        )
    elif len(event.pattern_match.group(1)) > 64:
        return await event.reply("Federation names cannot be over 64 characters long.")
    name = fedowner[1]
    fed_id = fedowner[0]
    new_name = event.pattern_match.group(1)
    db.rename_fed(fed_id, new_name)
    final_text = f"Tada! I've renamed your federation from '{name}' to '{new_name}'. (FedID: `{fed_id}`)."
    await event.reply(final_text)


@Cbot(pattern="^/joinfed ?(.*)")
async def jfed(event):
    if event.is_private:
        return await event.reply("Only supergroups can join feds.")
    if not event.is_group and not event.is_private:
        return await join_fed_channel(event)
    if event.from_id:
        if not await is_owner(event, event.sender_id):
            return
        args = event.pattern_match.group(1)
        if not args:
            return await event.reply(
                "You need to specify which federation you're asking about by giving me a FedID!"
            )
        if len(args) < 10:
            return await event.reply("This isn't a valid FedID format!")
        getfed = db.search_fed_by_id(args)
        if not getfed:
            return await event.reply(
                "This FedID does not refer to an existing federation."
            )
        name = getfed["fedname"]
        fed_id = db.get_chat_fed(event.chat_id)
        if fed_id:
            db.chat_leave_fed(fed_id, event.chat_id)
        db.chat_join_fed(args, event.chat_id)
        await event.reply(
            f'Successfully joined the "{name}" federation! All new federation bans will now also remove the members from this chat.'
        )


@Cbot(pattern="^/leavefed$")
async def lfed(event):
    if event.is_private:
        return await event.reply("Only supergroups can join/leave feds.")
    if not event.is_group and not event.is_private:
        return await leave_fed_channel(event)
    if event.from_id:
        if not await is_owner(event, event.sender_id):
            return
    fed_id = db.get_chat_fed(event.chat_id)
    if fed_id:
        fname = (db.search_fed_by_id(args))["fname"]
        await event.reply(
            'Chat {} has left the "{}" federation.'.format(event.chat.title, fname)
        )
        db.chat_leave_fed(fed_id, event.chat_id)
    else:
        await event.reply("This chat isn't currently in any federations!")


@Cbot(pattern="^/fpromote ?(.*)")
async def fp(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await anonymous_f_promote(event)
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    fedowner = db.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply(
            "Only federation creators can promote people, and you don't seem to have a federation to promote to!"
        )
    fname = fedowner[1]
    fed_id = fedowner[0]
    if user.id == event.sender_id:
        return await event.reply("Yeah well you are the fed owner!")
    fban, fbanreason, fbantime = db.get_fban_user(fed_id, user.id)
    if fban:
        if fbanreason:
            reason = "\n\nReason: <code>{fbanreason}</code>"
        else:
            reason = ""
        txt = f"User <a href='tg://user?id={user.id}'>{user.first_name}</a> is fbanned in {fname}. You should unfban them before promoting.{reason}"
        return await event.reply(txt, parse_mode="html")
    getuser = db.search_user_in_fed(fed_id, user.id)
    if getuser:
        return await event.reply(
            f"<a href='tg://user?id={user.id}'>{user.first_name}</a> is already an admin in {fname}!",
            parse_mode="html",
        )
    cb_data = str(event.sender_id) + "|" + str(user.id)
    ftxt = f"Please get <a href='tg://user?id={user.id}'>{user.first_name}</a> to confirm that they would like to be fed admin for {fname}"
    buttons = [
        Button.inline("Accept", data=f"fp_{cb_data}"),
        Button.inline("Decline", data=f"nofp_{cb_data}"),
    ]
    await event.respond(ftxt, buttons=buttons, parse_mode="html")


@Cinline(pattern=r"fp(\_(.*))")
async def fp_cb(event):
    input = ((event.pattern_match.group(1)).decode()).split("_", 1)[1]
    owner_id, user_id = input.split("|")
    owner_id = int(owner_id.strip())
    user_id = int(user_id.strip())
    fedowner = db.get_user_owner_fed_full(owner_id)
    fname = fedowner[1]
    fed_id = fedowner[0]
    if not event.sender_id == user_id:
        return await event.answer("You are not the user being fpromoted", alert=True)
    name = (await tbot.get_entity(user_id)).first_name
    db.user_join_fed(fed_id, user_id)
    res = f"User <a href='tg://user?id={user_id}'>{name}</a> is now an admin of {fname} (<code>{fed_id}</code>)"
    await event.edit(res, parse_mode="html")


@Cinline(pattern=r"nofp(\_(.*))")
async def nofp(event):
    tata = event.pattern_match.group(1)
    pata = tata.decode()
    input = pata.split("_", 1)[1]
    owner_id, user_id = input.split("|")
    owner_id = int(owner_id.strip())
    user_id = int(user_id.strip())
    fedowner = db.get_user_owner_fed_full(owner_id)
    if event.sender_id == owner_id:
        user = await tbot.get_entity(owner_id)
        await event.edit(
            f"Fedadmin promotion cancelled by <a href='tg://user?id={user.id}'>{user.first_name}</a>",
            parse_mode="html",
        )
    elif event.sender_id == user_id:
        user = await tbot.get_entity(user_id)
        await event.edit(
            f"Fedadmin promotion has been refused by <a href='tg://user?id={user.id}'>{user.first_name}</a>",
            parse_mode="html",
        )
    else:
        await event.answer("You are not the user being fpromoted")


@Cbot(pattern="^/fdemote ?(.*)")
async def fd(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await anonymous_f_demote(event)
    user = None
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    fedowner = db.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply(
            "Only federation creators can demote people, and you don't seem to have a federation to promote to!"
        )
    fname = fedowner[1]
    fed_id = fedowner[0]
    if not db.search_user_in_fed(fed_id, user.id):
        return await event.reply(
            f"This person isn't a federation admin for '{fname}', how could I demote them?"
        )
    db.user_demote_fed(fed_id, user.id)
    await event.reply(
        f"User <a href='tg://user?id={user.id}'>{user.first_name}</a> is no longer an admin of {fname} ({fed_id})",
        parse_mode="html",
    )


@Cbot(pattern="^/ftransfer ?(.*)")
async def ft(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await anonymous_f_transfer(event)
    sender_id = event.sender_id
    user_r = None
    if not await is_admin(event.chat_id, sender_id):
        return await event.reply("Only admins can execute this command!")
    try:
        user_r, extra = await get_user(event)
    except TypeError:
        pass
    if not user_r:
        return
    if user_r.bot:
        return await event.reply("Bots can't own federations.")
    fedowner = db.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply("You don't have a fed to transfer!")
    fname = fedowner[1]
    fed_id = fedowner[0]
    if user_r.id == sender_id:
        return await event.reply("You can only transfer your fed to others!")
    ownerfed = db.get_user_owner_fed_full(user_r.id)
    if ownerfed:
        return await event.reply(
            f"<a href='tg://user?id={user_r.id}'>{user_r.first_name}</a> already owns a federation - they can't own another.",
            parse_mode="html",
        )
    getuser = db.search_user_in_fed(fed_id, user_r.id)
    if not getuser:
        return await event.reply(
            f"<a href='tg://user?id={user_r.id}'>{user_r.first_name}</a> isn't an admin in {fname} - you can only give your fed to other admins.",
            parse_mode="html",
        )
    cb_data = str(sender_id) + "|" + str(user_r.id)
    text = f"<a href='tg://user?id={user_r.id}'>{user_r.first_name}</a>, please confirm you would like to receive fed {fname} (<code>{fed_id}</code>) from <a href='tg://user?id={sender_id}'>{event.sender.first_name}</a>"
    buttons = [
        Button.inline("Accept", data=f"ft_{cb_data}"),
        Button.inline("Decline", data=f"noft_{cb_data}"),
    ]
    await event.respond(text, buttons=buttons, parse_mode="html")

@Cinline(pattern=r"ft(\_(.*))")
async def ft(event):
    input = ((event.pattern_match.group(1)).decode()).split("_", 1)[1]
    input = input.split("|", 1)
    owner_id = int(input[0])
    user_id = int(input[1])
    if not event.sender_id == user_id:
        return await event.answer("This action is not intended for you.", alert=True)
    fedowner = db.get_user_owner_fed_full(owner_id)
    fed_id = fedowner[1]
    fname = fedowner[0]
    try:
        owner = await tbot.get_entity(owner_id)
    except:
        return
    e_text = f"<a href='tg://user?id={owner.id}'>{owner.first_name}</a>, please confirm that you wish to send fed {fname} (<code>{fed_id}</code>) to <a href='tg://user?id={event.sender_id}'>{event.sender.first_name}</a> this cannot be undone."
    cb_data = str(owner.id) + "|" + str(user_id)
    buttons = [
        Button.inline("Confirm", data=f"ftc_{cb_data}"),
        Button.inline("Cancel", data=f"ftnoc_{cb_data}"),
    ]
    await event.edit(e_text, buttons=buttons, parse_mode="html")


@Cinline(pattern=r"noft(\_(.*))")
async def noft(event):
    input = ((event.pattern_match.group(1)).decode()).split("_", 1)[1]
    input = input.split("|", 1)
    owner_id = int(input[0])
    user_id = int(input[1])
    if not event.sender_id in [user_id, owner_id]:
        return await event.answer("This action is not intended for you.", alert=True)
    if event.sender_id == owner_id:
        user_name = ((event.sender.first_name).replace("<", "&lt;")).replace(
            ">", "&gt;"
        )
        o_text = (
            "<a href='tg://user?id={}'>{}</a> has cancelled the fed transfer.".format(
                owner_id, user_name
            )
        )
    elif event.sender_id == user_id:
        user_name = ((event.sender.first_name).replace("<", "&lt;")).replace(
            ">", "&gt;"
        )
        o_text = (
            "<a href='tg://user?id={}'>{}</a> has declined the fed transfer.".format(
                owner_id, user_name
            )
        )
    await event.edit(o_text, parse_mode="html", buttons=None)


ftransfer_log = """
<b>Fed Transfer</b>
<b>Fed:</b> {}
<b>New Fed Owner:</b> <a href='tg://user?id={}'>{}</a> - <code>{}</code>
<b>Old Fed Owner:</b> <a href='tg://user?id={}'>{}</a> - <code>{}</code>

<a href='tg://user?id={}'>{}</a> is now the fed owner. They can promote/demote admins as they like.
"""


@Cinline(pattern=r"ftc(\_(.*))")
async def noft(event):
    input = ((event.pattern_match.group(1)).decode()).split("_", 1)[1]
    input = input.split("|", 1)
    owner_id = int(input[0])
    user_id = int(input[1])
    if not event.sender_id == owner_id:
        return await event.answer("This action is not intended for you.", alert=True)
    f_text = "Congratulations! Federation {} (<code>{}</code>) has successfully been transferred from <a href='tg://user?id={}'>{}</a> to <a href='tg://user?id={}'>{}</a>."
    o_name = ((event.sender.first_name).replace("<", "&lt;")).replace(">", "&gt;")
    n_name = (
        ((await tbot.get_entity(user_id)).first_name).replace("<", "&lt;")
    ).replace(">", "&gt;")
    fedowner = db.get_user_owner_fed_full(owner_id)
    fed_id = fedowner[0]
    fname = fedowner[1]
    await event.edit(
        f_text.format(fname, fed_id, owner_id, o_name, user_id, n_name),
        parse_mode="html",
    )
    db.transfer_fed(event.sender_id, user_id)
    await event.respond(
        ftransfer_log.format(
            fname, user_id, n_name, user_id, owner_id, o_name, owner_id, user_id, n_name
        ),
        parse_mode="html",
    )


@Cinline(pattern=r"ftnoc(\_(.*))")
async def noft(event):
    input = ((event.pattern_match.group(1)).decode()).split("_", 1)[1]
    input = input.split("|", 1)
    owner_id = int(input[0])
    if not event.sender_id == owner_id:
        return await event.answer("This action is not intended for you.", alert=True)
    await event.edit(
        "Fed transfer has been cancelled by <a href='tg://user?id={owner_id}'>{event.sender.first_name}</a>.",
        parse_mode="html",
    )


@Cbot(pattern="^/fednotif ?(.*)")
async def fed_notif(event):
    if not event.is_private:
        return await event.reply("This command is made to be used in PM.")
    args = event.pattern_match.group(1)
    fedowner = db.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply("You aren't the creator of any feds to act in.")
    fname = fedowner[1]
    if not args:
        mode = db.user_feds_report(event.sender_id)
        if mode:
            f_txt = "The `{}` fed is currently sending notifications to it's creator when a fed action is performed."
        else:
            f_txt = "The `{}` fed is currently **NOT** sending notifications to it's creator when a fed action is performed."
        await event.reply(f_txt.format(fname))
    elif args in ["on", "yes"]:
        await event.reply(
            f"The fed silence setting for `{fname}` has been updated to: `true`"
        )
        db.set_feds_setting(event.sender_id, True)
    elif args in ["off", "no"]:
        await event.reply(
            f"The fed silence setting for `{fname}` has been updated to: `false`"
        )
        db.set_feds_setting(event.sender_id, False)
    else:
        await event.reply("Your input was not recognised as one of: yes/no/on/off")




new_fban = """
<b>New FedBan</b>
<b>Fed:</b> {}
<b>FedAdmin:</b> <a href="tg://user?id={}">{}</a>
<b>User:</b> <a href="tg://user?id={}">{}</a>
<b>User ID:</b> <code>{}</code>
"""
update_fban = """
<b>FedBan Reason Update</b>
<b>Fed:</b> {}
<b>FedAdmin:</b> <a href='tg://user?id={}'>{}</a>
<b>User:</b> <a href='tg://user?id={}'>{}</a>
<b>User ID:</b> <code>{}</code>{}
<b>New Reason:</b> {}
"""
un_fban = """
<b>New un-FedBan</b>
<b>Fed:</b> {}
<b>FedAdmin:</b> <a href="tg://user?id={}">{}</a>
<b>User:</b> <a href="tg://user?id={}">{}</a>
<b>User ID:</b> <code>{}</code>
"""


@Cbot(pattern="^/fban ?(.*)")
async def fban(event):
    if (
        event.text.startswith("/fbanstat")
        or event.text.startswith(".fbanstat")
        or event.text.startswith("!fbanstat")
        or event.text.startswith("?fbanstat")
    ):
        return
    if event.is_group:
        fed_id = db.get_chat_fed(event.chat_id)
        if not fed_id:
            return await event.reply("This chat isn't in any federations.")
        mejik = db.search_fed_by_id(fed_id)
        fname = mejik["fedname"]
        if not is_user_fed_admin(fed_id, event.sender_id):
            return await event.reply(f"You aren't a federation admin for {fname}!")
        owner_id = mejik["owner_id"]
    elif event.is_private:
        fedowner = db.get_user_owner_fed_full(event.sender_id)
        if not fedowner:
            return await event.reply("You aren't the creator of any feds to act in.")
        fed_id = fedowner[0]
        fname = fedowner[1]
        owner_id = event.sender_id
    if event.reply_to:
        user = (await event.get_reply_message()).sender
        try:
            reason = event.text.split(None, 1)[1]
        except:
            reason = None
    elif event.pattern_match.group(1):
        u = event.text.split(None, 2)
        try:
            u_ent = u[1]
            if u[1].isnumeric():
                u_ent = int(u[1])
            user = await tbot.get_entity(u_ent)
        except:
            return await event.reply(
                "I don't know who you're talking about, you're going to need to specify a user...!"
            )
        try:
            reason = u[2]
        except:
            reason = None
    else:
        return await event.reply(
            "I don't know who you're talking about, you're going to need to specify a user...!"
        )
    if reason:
        if len(reason) > 1024:
            reason = (
                reason[:1024]
                + "\n\nNote: The fban reason was over 1024 characters, so has been truncated."
            )
    if user.id == BOT_ID:
        return await event.reply(
            "Oh you're a funny one aren't you! I am _not_ going to fedban myself."
        )
    elif user.id in ADMINS:
        return await event.reply("I'm not banning one of my sudo users.")
    elif is_user_fed_admin(fed_id, user.id):
        f_ad = f"I'm not banning a fed admin/owner from their own fed! ({fname})"
        return await event.reply(f_ad)
    fban, fbanreason, fbantime = db.get_fban_user(fed_id, user.id)
    if fban:
        if reason == "" and fbanreason == "":
            return await event.reply(
                "User <a href='tg://user?id={}'>{}</a> is already banned in {}. There is no reason set for their fedban yet, so feel free to set one.".format(
                    user.id, user.first_name, fname
                ),
                parse_mode="html",
            )
        elif reason == fbanreason:
            return await event.reply(
                "User <a href='tg://user?id={}'>{}</a> has already been fbanned, with the exact same reason.".format(
                    user.id, user.first_name
                ),
                parse_mode="html",
            )
        elif reason == None:
            if not fbanreason:
                return await event.reply(
                    "User <a href='tg://user?id={}'>{}</a> is already banned in {}.".format(
                        user.id, user.first_name, fname
                    ),
                    parse_mode="html",
                )
            else:
                return await event.reply(
                    "User <a href='tg://user?id={}'>{}</a> is already banned in {}, with reason:\n<code>{}</code>.".format(
                        user.id, user.first_name, fname, fbanreason
                    ),
                    parse_mode="html",
                )
        db.fban_user(
            fed_id,
            user.id,
            user.first_name,
            user.last_name,
            reason,
            str(time.time()),
        )
        if fbanreason:
            p_reason = f"\n<b>Previous Reason:</b> {fbanreason}"
        fban_global_text = update_fban.format(
            fname,
            event.sender_id,
            event.sender.first_name,
            user.id,
            user.first_name,
            user.id,
            p_reason,
            reason,
        )
    else:
        sql.fban_user(
            fed_id,
            user.id,
            user.first_name,
            user.last_name,
            reason,
            int(time.time()),
        )
        fban_global_text = new_fban.format(
            fname,
            event.sender_id,
            event.sender.first_name,
            user.id,
            user.first_name,
            user.id,
            reason,
        )
        if reason:
            fban_global_text = fban_global_text + f"\n<b>Reason:</b> {reason}"
    await event.respond(fban_global_text, parse_mode="html")
    getfednotif = db.user_feds_report(int(owner_id))
    if getfednotif and event.chat_id != int(owner_id):
        await tbot.send_message(int(owner_id), fban_global_text, parse_mode="html")
    log_c = db.get_fed_log(fed_id)
    if log_c and event.chat_id != int(log_c):
        await tbot.send_message(int(log_c), fban_global_text, parse_mode="html")
    fed_chats = list(db.get_all_fed_chats(fed_id))
    if len(fed_chats) != 0:
        for c in fed_chats:
            try:
                await tbot.edit_permissions(int(c), view_messages=False)
            except:
                pass
    subs = list(sql.get_subscriber(fed_id))
    if len(subs) != 0:
        for fed in subs:
            sql.fban_user(
                fed,
                user.id,
                user.first_name,
                user.last_name,
                user.username,
                reason,
                int(time.time()),
            )
            all_fedschat = sql.all_fed_chats(fed)
            for c in all_fedschat:
                try:
                    await tbot.edit_permissions(int(c), view_messages=False)
                except:
                    pass


@Cbot(pattern="^/unfban ?(.*)")
async def unfban(event):
    if event.is_group:
        fed_id = sql.get_fed_id(event.chat_id)
        if not fed_id:
            return await event.reply("This chat isn't in any federations.")
        mejik = sql.get_fed_info(fed_id)
        fname = mejik["fname"]
        if not is_user_fed_admin(fed_id, event.sender_id):
            return await event.reply(f"You aren't a federation admin for {fname}!")
        owner_id = mejik["owner"]
    elif event.is_private:
        fedowner = sql.get_user_owner_fed_full(event.sender_id)
        if not fedowner:
            return await event.reply("You aren't the creator of any feds to act in.")
        fed_id = fedowner[0]["fed_id"]
        fname = fedowner[0]["fed"]["fname"]
        owner_id = event.sender_id
    if event.reply_to:
        user = (await event.get_reply_message()).sender
        try:
            reason = event.text.split(None, 1)[1]
        except:
            reason = None
    elif event.pattern_match.group(1):
        u = event.text.split(None, 2)
        try:
            u_ent = u[1]
            if u[1].isnumeric():
                u_ent = int(u[1])
            user = await tbot.get_entity(u_ent)
        except:
            return await event.reply(
                "I don't know who you're talking about, you're going to need to specify a user...!"
            )
        try:
            reason = u[2]
        except:
            reason = None
    else:
        return await event.reply(
            "I don't know who you're talking about, you're going to need to specify a user...!"
        )
    if reason:
        if len(reason) > 1024:
            reason = (
                reason[:1024]
                + "\n\nNote: The unfban reason was over 1024 characters, so has been truncated."
            )
    if user.id == BOT_ID:
        return await event.reply(
            "Oh you're a funny one aren't you! How do you think I would have fbanned myself hm?."
        )
    fban, fbanreason, fbantime = sql.get_fban_user(fed_id, user.id)
    if not fban:
        g_string = (
            "This user isn't banned in the current federation, {}. (`{}`)".format(
                fname, fed_id
            )
        )
        return await event.reply(g_string)
    ufb_string = un_fban.format(
        fname,
        event.sender_id,
        event.sender.first_name,
        user.id,
        user.first_name,
        user.id,
    )
    if reason:
        ufb_string = ufb_string + f"\n<b>Reason:</b> {reason}"
    sql.un_fban_user(fed_id, user.id)
    await event.respond(ufb_string, parse_mode="html")
    getfednotif = sql.user_feds_report(int(owner_id))
    if getfednotif and event.chat_id != int(owner_id):
        await tbot.send_message(int(owner_id), ufb_string, parse_mode="html")
    log_c = sql.get_fed_log(fed_id)
    if log_c and event.chat_id != int(log_c):
        await tbot.send_message(int(log_c), ufb_string, parse_mode="html")


@Cbot(pattern="^/chatfed")
async def CF(c):
    if c.is_private:
        return
    if c.is_group:
        if not await is_admin(c.chat_id, c.sender_id):
            return await c.reply("You need to be an admin to do this.")
    fed_id = sql.get_fed_id(c.chat_id)
    if not fed_id:
        return await c.reply("This chat isn't part of any feds yet!")
    fname = (sql.get_fed_info(fed_id))["fname"]
    c_f = "Chat {} is part of the following federation: {} (ID: `{}`)".format(
        c.chat.title, fname, fed_id
    )
    await c.reply(c_f)


fed_info = """
Fed info:
FedID: <code>{}</code>
Name: {}
Creator: <a href="tg://user?id={}">this person</a> (<code>{}</code>)
Number of admins: <code>{}</code>
Number of bans: <code>{}</code>
Number of connected chats: <code>{}</code>
Number of subscribed feds: <code>{}</code>
"""


@Cbot(pattern="^/fedinfo ?(.*)")
async def finfo(event):
    if event.is_group:
        if not await is_admin(event.chat_id, event.sender_id):
            return await event.reply("This command can only be used in private.")
    fedowner = sql.get_user_owner_fed_full(event.sender_id)
    input = event.pattern_match.group(1)
    if not input and not fedowner:
        return await event.reply(
            "You need to give me a FedID to check, or be a federation creator to use this command!"
        )
    elif input:
        if len(input) < 10:
            return await event.reply("This isn't a valid FedID format!")
        getfed = sql.search_fed_by_id(input)
        if not getfed:
            return await event.reply(
                "This FedID does not refer to an existing federation."
            )
        fname = getfed["fname"]
        fed_id = input
    elif fedowner:
        fed_id = fedowner[0]["fed_id"]
        fname = fedowner[0]["fed"]["fname"]
    info = sql.get_fed_info(fed_id)
    fadmins = len(sql.all_fed_users(fed_id))
    fbans = len(sql.get_all_fban_users(fed_id))
    fchats = len(sql.all_fed_chats(fed_id))
    subbed = len(sql.get_subscriber(fed_id))
    fed_main = fed_info.format(
        fed_id,
        fname,
        int(info["owner"]),
        int(info["owner"]),
        fadmins,
        fbans,
        fchats,
        subbed,
    )
    sql.get_mysubs(fed_id)
    await event.reply(fed_main, parse_mode="html")

@Cbot(pattern="^/subfed ?(.*)")
async def s_fed(event):
    fedowner = sql.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply(
            "Only federation creators can subscribe to a fed. But you don't have a federation!"
        )
    arg = event.pattern_match.group(1)
    if not arg:
        return await event.reply(
            "You need to specify which federation you're asking about by giving me a FedID!"
        )
    if len(arg) < 10:
        return await event.reply("This isn't a valid FedID format!")
    getfed = sql.search_fed_by_id(arg)
    if not getfed:
        return await event.reply("This FedID does not refer to an existing federation.")
    s_fname = getfed["fname"]
    if arg == fedowner[0]["fed_id"]:
        return await event.reply("... What's the point in subscribing a fed to itself?")
    if len(sql.get_all_subs(str(fedowner[0]["fed_id"]))) > 5:
        return await event.reply(
            "You can subscribe to at most 5 federations. Please unsubscribe from other federations before adding more."
        )
    await event.reply(
        "Federation `{}` has now subscribed to `{}`. All fedbans in `{}` will now take effect in both feds.".format(
            fedowner[0]["fed"]["fname"], s_fname, s_fname
        )
    )
    sql.subs_fed(arg, fedowner[0]["fed_id"])


@Cbot(pattern="^/unsubfed ?(.*)")
async def us_fed(event):
    fedowner = sql.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply(
            "Only federation creators can unsubscribe to a fed. But you don't have a federation!"
        )
    arg = event.pattern_match.group(1)
    if not arg:
        return await event.reply(
            "You need to specify which federation you're asking about by giving me a FedID!"
        )
    if len(arg) < 10:
        return await event.reply("This isn't a valid FedID format!")
    getfed = sql.search_fed_by_id(arg)
    if not getfed:
        return await event.reply("This FedID does not refer to an existing federation.")
    await event.reply(
        "Federation `{}` is no longer subscribed to `{}`. Bans in `{}` will no longer be applied. Please note that any bans that happened because the user was banned from the subfed will need to be removed manually.".format(
            fedowner[0]["fed"]["fname"], getfed["fname"], getfed["fname"]
        )
    )
    sql.unsubs_fed(arg, fedowner[0]["fed_id"])

# balance tomorrow
# afk balance tomorrow
# add mass fban
# add fban reason compulsory
# kek
