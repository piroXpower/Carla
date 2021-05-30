import uuid

from telethon import Button

import Evelyn.modules.sql.feds_sql as sql
from Evelyn import BOT_ID, OWNER_ID
from Evelyn.events import Cbot

from . import ELITES, SUDO_USERS

# in_bannable
ELITES.append(OWNER_ID)
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
   await event.edit("You have deleted your federation! All chats linked to it are now federation-less.")

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
   args = event.patter_match.group(1)
   if not args:
      return await event.reply("You need to specify which federation you're asking about by giving me a FedID!")
   if len(args) < 10:
     return await event.reply("This isn't a valid FedID format!")
   getfed = sql.search_fed_by_id(args)
   name = getfed["fname"]
   if not getfed:
      return await event.reply("This FedID does not refer to an existing federation.")
   fed_id = sql.get_fed_id(event.chat_id)
   if fed_id:
       sql.chat_leave_fed(event.chat_id)
   sql.chat_join_fed(args, event.chat.title, event.chat_id)
   await event.reply(f'Successfully joined the "{name}" federation! All new federation bans will now also remove the members from this chat.')
 
