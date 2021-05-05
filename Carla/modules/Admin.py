from Carla import tbot, OWNER_ID
from Carla.events import Cbot
from . import ELITES, can_promote_users, get_user, is_admin

@Cbot(pattern="^/promote ?(.*)")
async def _(event):
 if event.is_private:
  return #connection
 if event.from_id:
  await can_promote_users(event.chat_id, event.sender_id)
  try:
   user, title = await get_user(event)
  except:
   return
  if not title:
    title = "Admin"
  if await is_admin(event.chat_id, user.id):
    return await event.reply("This User is already an Admin!")
  try:
    await tbot.edit_admin(event.chat_id, user.id, manage_call=False, add_admins=False, pin_messages=True, delete_messages=True, ban_users=True, change_info=True, invite_users=True) 
    await event.respond(f"Promoted **{user.first_name}** in **{event.chat.title}**.")
  except:
    await event.reply("Seems like I don't have enough rights to do that.")
 else:
   await anonymous(event, promote)

@Cbot(pattern="^/superpromote ?(.*)")
async def _(event):
 if event.is_private:
  return #connection
 if event.from_id:
  await can_promote_users(event.chat_id, event.sender_id)
  try:
   user, title = await get_user(event)
  except:
   return
  if not title:
    title = "Admin"
  if await is_admin(event.chat_id, user.id):
    return await event.reply("This User is already an Admin!")
  try:
    await tbot.edit_admin(event.chat_id, user.id, manage_call=True, add_admins=True, pin_messages=True, delete_messages=True, ban_users=True, change_info=True, invite_users=True) 
    await event.respond(f"Promoted **{user.first_name}** in **{event.chat.title}** with full Rights.")
  except:
    await event.reply("Seems like I don't have enough rights to do that.")
 else:
   await anonymous(event, promote)


async def anonymous(event, mode):
  print(mode)

