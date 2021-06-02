import uuid

from telethon import Button, events

import Evelyn.modules.sql.feds_sql as sql
from Evelyn import BOT_ID, OWNER_ID
from Evelyn.events import Cbot

from . import ELITES, SUDO_USERS, get_user, is_admin, is_owner

# in_bannable
ELITES.append(BOT_ID)
ADMINS = ELITES + SUDO_USERS


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
 fedowner = get_user_owner_fed_full(event.sender_id)
 if not fedowner:
   return await event.reply("Only federation creators can promote people, and you don't seem to have a federation to promote to!")
 fname = fedowner[0]["fed"]["fname"]
 fed_id = fedowner[0]["fed_id"]
 if user.id == event.sender_id:
    return await event.reply("Yeah well you are the fed owner!")
 fban, fbanreason, fbantime = get_fban_user(fed_id, int(user.id))
 if fban:
   if fbanreason:
     reason = "\n\nReason: <code>{fbanreason}</code>"
   else:
     reason = ""
   txt = f"User <a href='tg://user?id={user.id}'>{user.first_name}</a> is fbanned in {fname}. You should unfban them before promoting.{reason}")
   return await event.reply(txt, parse_mode="html")
 getuser = search_user_in_fed(fed_id, user.id)
 if getuser:
   return await event.reply(f"<a href='tg://user?id={user.id}'>{user.first_name}</a> is already an admin in {fname}!", parse_mode="html")
 cb_data = str(event.sender_id) + "|" + str(user.id)
 ftxt = f"Please get <a href='tg://user?id={user.id}'>{user.first_name}</a> to confirm that they would like to be fed admin for {fname}"
 buttons = [
        Button.inline("Accept", data=f"fp_{cb_data}"),
        Button.inline("Decline", data=f"nofp_{cb_data}"),
    ]
 await event.respond(ftxt, buttons=buttons, parse_mode="html")

@tbot.on(events.CallbackQuery(pattern=r"fp(\_(.*))"))
async def fp_cb(event):
 data = (event.pattern_match.group(1)).decode
 input = data.split("_", 1)[1]
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
 data = (event.pattern_match.group(1)).decode
 input = data.split("_", 1)[1]
 owner_id, user_id = input.split("|")
 owner_id = int(owner_id.strip())
 user_id = int(user_id.strip())
 fedowner = sql.get_user_owner_fed_full(owner_id)
 fname = fedowner[0]["fed"]["fname"]
 fed_id = fedowner[0]["fed_id"]
 if event.sender_id == owner_id:
   user = await tbot.get_entity(owner_id)
   await event.edit(f"Fedadmin promotion cancelled by <a href='tg://user?id={user.id}'>{user.first_name}</a>", parse_mode="html")
 elif event.sender_id == user_id:
   user = await tbot.get_entity(user_id)
   await event.edit(f"Fedadmin promotion has been refused by <a href='tg://user?id={user.id}'>{user.first_name}</a>", parse_mode="html")
 else:
   await event.answer("You are not the user being fpromoted")


@Cbot(pattern="^/(ftransfer|Fedtransfer|fedtransfer|Ftransfer|transferfed)")
async def ft(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await anonymous_f_transfer(event)
    sender_id = event.sender_id
    user = None
    if not await is_admin(event.chat_id, sender_id):
        return await event.reply("Only admins can execute this command!")
    try:
        user, extra = await get_user(event)
    except TypeError:
        pass
    if not user:
        return
    if user.bot:
        return await event.reply("Bots can't own federations.")
    fedowner = sql.get_user_owner_fed_full(event.sender_id)
    if not fedowner:
        return await event.reply("You don't have a fed to transfer!")
    fname = fedowner[0]["fed"]["fname"]
    fed_id = fedowner[0]["fed_id"]
    if user.id == sender_id:
        return await event.reply("You can only transfer your fed to others!")
    ownerfed = sql.get_user_owner_fed_full(user.id)
    if ownerfed:
        return await event.reply(
            f"<a href='tg://user?id={user.id}'>{user.first_name}</a> already owns a federation - they can't own another.",
            parse_mode="html",
        )
    getuser = sql.search_user_in_fed(fed_id, user.id)
    if not getuser:
        return await event.reply(
            f"<a href='tg://user?id={user.id}'>{user.first_name}</a> isn't an admin in {fname} - you can only give your fed to other admins.",
            parse_mode="html",
        )
    cb_data = str(sender_id) + "|" + str(user.id)
    text = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>, please confirm you would like to receive fed {fname} (`{fed_id}`) from <a href='tg://user?id={sender_id}'>{event.sender.first_name}</a>"
    buttons = [
        Button.inline("Accept", data=f"ft_{cb_data}"),
        Button.inline("Decline", data=f"noft_{cb_data}"),
    ]
    await event.respond(text, buttons=buttons)


# soon
# eye some pain
