import uuid

from telethon import Button, events

import Evelyn.modules.sql.feds_sql as sql
from Evelyn import BOT_ID, OWNER_ID
from Evelyn.events import Cbot

from . import ELITES, SUDO_USERS, get_user, is_admin, is_owner

# in_bannable
ADMINS = ELITES + SUDO_USERS
ADMINS.append(BOT_ID)


def is_user_fed_admin(fed_id, user_id):
    fed_admins = sql.all_fed_users(fed_id)
    if fed_admins is False:
        return False
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
    f_owner = sql.get_user_owner_fed_full(event.sender_id)
    if f_owner:
        fed_name = f_owner[0]["fed"]["fname"]
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
    sql.new_fed(event.sender_id, name, fed_id)
    await event.reply(
        f"Created new federation with FedID: `{fed_id}`.\nUse this ID to join the federation! eg:\n`/joinfed {fed_id}`"
    )


@Cbot(pattern="^/delfed")
async def del_fed(event):
    if not event.is_private:
        return await event.reply("Delete your federation in my PM - not in a group.")
    fedowner = sql.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply("It doesn't look like you have a federation yet!")
    name = fedowner[0]["fed"]["fname"]
    fed_id = fedowner[0]["fed_id"]
    await tbot.send_message(
        event.chat_id,
        "Are you sure you want to delete your federation? This action cannot be undone - you will lose your entire ban list, and '{}' will be permanently gone.".format(
            name
        ),
        buttons=[
            [Button.inline("Delete Federation", data="rmfed_{}".format(fed_id))],
            [Button.inline("Cancel", data="cancel_delete")],
        ],
    )


@tbot.on(events.CallbackQuery(pattern=r"rmfed(\_(.*))"))
async def delete_fed(event):
    tata = event.pattern_match.group(1)
    data = tata.decode()
    fed_id = data.split("_", 1)[1]
    sql.del_fed(fed_id)
    await event.edit(
        "You have deleted your federation! All chats linked to it are now federation-less."
    )


@tbot.on(events.CallbackQuery(pattern=r"cancel_delete"))
async def delete_fed(event):
    await event.edit("Federation deletion cancelled.")


@Cbot(pattern="^/renamefed ?(.*)")
async def rename(event):
    if not event.is_private:
        return await event.reply("You can only rename your fed in PM.")
    fedowner = sql.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply("It doesn't look like you have a federation yet!")
    if not event.pattern_match.group(1):
        return await event.reply(
            "You need to give your federation a new name! Federation names can be up to 64 characters long."
        )
    elif len(event.pattern_match.group(1)) > 64:
        return await event.reply("Federation names cannot be over 64 characters long.")
    name = fedowner[0]["fed"]["fname"]
    fed_id = fedowner[0]["fed_id"]
    new_name = event.pattern_match.group(1)
    sql.rename_fed(fed_id, event.sender_id, new_name)
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
        getfed = sql.search_fed_by_id(args)
        name = getfed["fname"]
        if not getfed:
            return await event.reply(
                "This FedID does not refer to an existing federation."
            )
        fed_id = sql.get_fed_id(event.chat_id)
        if fed_id:
            sql.chat_leave_fed(event.chat_id)
        sql.chat_join_fed(args, event.chat.title, event.chat_id)
        await event.reply(
            f'Successfully joined the "{name}" federation! All new federation bans will now also remove the members from this chat.'
        )


@Cbot(pattern="^/leavefed$")
async def lfed(event):
    if event.is_private:
        return await event.reply("Only supergroups can join/leave feds.")
    if not event.is_group and not event.is_private:
        return await leave_fed_channel(event)


# soon
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
    fedowner = sql.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply(
            "Only federation creators can promote people, and you don't seem to have a federation to promote to!"
        )
    fname = fedowner[0]["fed"]["fname"]
    fed_id = fedowner[0]["fed_id"]
    if user.id == event.sender_id:
        return await event.reply("Yeah well you are the fed owner!")
    fban, fbanreason, fbantime = sql.get_fban_user(fed_id, int(user.id))
    if fban:
        if fbanreason:
            reason = "\n\nReason: <code>{fbanreason}</code>"
        else:
            reason = ""
        txt = f"User <a href='tg://user?id={user.id}'>{user.first_name}</a> is fbanned in {fname}. You should unfban them before promoting.{reason}"
        return await event.reply(txt, parse_mode="html")
    getuser = sql.search_user_in_fed(fed_id, user.id)
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


@tbot.on(events.CallbackQuery(pattern=r"fp(\_(.*))"))
async def fp_cb(event):
    tata = event.pattern_match.group(1)
    pata = tata.decode()
    input = pata.split("_", 1)[1]
    owner_id, user_id = input.split("|")
    owner_id = int(owner_id.strip())
    user_id = int(user_id.strip())
    fedowner = sql.get_user_owner_fed_full(owner_id)
    fname = fedowner[0]["fed"]["fname"]
    fed_id = fedowner[0]["fed_id"]
    name = (await tbot.get_entity(user_id)).first_name
    if not event.sender_id == user_id:
        return await event.answer("You are not the user being fpromoted")
    sql.user_join_fed(fed_id, user_id)
    res = f"User <a href='tg://user?id={user_id}'>{name}</a> is now an admin of {fname} (`{fed_id}`)"
    await event.edit(res, parse_mode="html")


@tbot.on(events.CallbackQuery(pattern=r"nofp(\_(.*))"))
async def nofp(event):
    tata = event.pattern_match.group(1)
    pata = tata.decode()
    input = pata.split("_", 1)[1]
    owner_id, user_id = input.split("|")
    owner_id = int(owner_id.strip())
    user_id = int(user_id.strip())
    fedowner = sql.get_user_owner_fed_full(owner_id)
    fedowner[0]["fed"]["fname"]
    fedowner[0]["fed_id"]
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
    fedowner = sql.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply(
            "Only federation creators can demote people, and you don't seem to have a federation to promote to!"
        )
    fname = fedowner[0]["fed"]["fname"]
    fed_id = fedowner[0]["fed_id"]
    if not sql.search_user_in_fed(fed_id, user.id):
        return await event.reply(
            f"This person isn't a federation admin for '{fname}', how could I demote them?"
        )
    sql.user_demote_fed(fed_id, user.id)
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
    fedowner = sql.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply("You don't have a fed to transfer!")
    fname = fedowner[0]["fed"]["fname"]
    fed_id = fedowner[0]["fed_id"]
    if user_r.id == sender_id:
        return await event.reply("You can only transfer your fed to others!")
    ownerfed = sql.get_user_owner_fed_full(user_r.id)
    if ownerfed:
        return await event.reply(
            f"<a href='tg://user?id={user_r.id}'>{user_r.first_name}</a> already owns a federation - they can't own another.",
            parse_mode="html",
        )
    getuser = sql.search_user_in_fed(fed_id, user_r.id)
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


@tbot.on(events.CallbackQuery(pattern=r"ft(\_(.*))"))
async def ft(event):
    input = ((event.pattern_match.group(1)).decode()).split("_", 1)[1]
    input = input.split("|", 1)
    owner_id = int(input[0])
    user_id = int(input[1])
    if not event.sender_id == user_id:
        return await event.answer("This action is not intended for you.", alert=True)
    fedowner = sql.get_user_owner_fed_full(owner_id)
    fed_id = fedowner[0]["fed_id"]
    fname = fedowner[0]["fed"]["fname"]
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


@tbot.on(events.CallbackQuery(pattern=r"noft(\_(.*))"))
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


@tbot.on(events.CallbackQuery(pattern=r"ftc(\_(.*))"))
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
    fedowner = sql.get_user_owner_fed_full(owner_id)
    fed_id = fedowner[0]["fed_id"]
    fname = fedowner[0]["fed"]["fname"]
    await event.edit(
        f_text.format(fname, fed_id, owner_id, o_name, user_id, n_name),
        parse_mode="html",
    )
    sql.transfer_fed(str(fed_id), user_id)
    await event.respond(
        ftransfer_log.format(
            fname, user_id, n_name, user_id, owner_id, o_name, owner_id, user_id, n_name
        ),
        parse_mode="html",
    )


@tbot.on(events.CallbackQuery(pattern=r"ftnoc(\_(.*))"))
async def noft(event):
    input = ((event.pattern_match.group(1)).decode()).split("_", 1)[1]
    input = input.split("|", 1)
    owner_id = int(input[0])
    int(input[1])
    if not event.sender_id == owner_id:
        return await event.answer("This action is not intended for you.", alert=True)
