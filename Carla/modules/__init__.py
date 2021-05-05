from Carla import tbot
from telethon import events, Button

async def can_promote_users(chat_id, user_id):
 perm = await tbot.get_permissions(chat_id, user_id)
 if not perm.is_admin:
  return await event.reply("You need to be an admin to do this.")
 if not perm.add_admins:
  return await event.reply("You are missing the following rights to use this command: CanPromoteUsers.")
 return True

async def can_change_info(chat_id, user_id):
 perm = await tbot.get_permissions(chat_id, user_id)
 if not perm.is_admin:
  return await event.reply("You need to be an admin to do this.")
 if not perm.change_info:
  return await event.reply("You are missing the following rights to use this command: CanChangeInfo.")
 return True

async def can_ban_users(chat_id, user_id):
 perm = await tbot.get_permissions(chat_id, user_id)
 if not perm.is_admin:
  return await event.reply("You need to be an admin to do this.")
 if not perm.ban_users:
  return await event.reply("You are missing the following rights to use this command: CanBanUsers.")
 return True

async def get_user(event):
    args = event.pattern_match.group(1).split(" ", 1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await tbot.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        extra = ""
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.reply("I don't know who you're talking about, you're going to need to specify a user...!")
            return
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return

    return user_obj, extra

