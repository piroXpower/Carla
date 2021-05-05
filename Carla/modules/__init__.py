from Carla import tbot


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
