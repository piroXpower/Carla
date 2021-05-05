from Carla import tbot, OWNER_ID
from Carla.events import Cbot
from . import ELITES, can_promote_users, get_user, is_admin

@Cbot(pattern="^/promote ?(.*)")
async def _(event):
 if event.is_private:
  return #connection
 if event.from_id:
  await can_promote_users(event.chat_id, event.sender_id)
  user, title = get_user(event)
  if not title:
    title = "Admin"
  if is_admin(event.chat_id, user.id):
    return await event.reply("This User is already an Admin!")
  try:
    await tbot.edit_admin(event.chat_id, user.id, is_admin=True, anonymous=False, add_admins=False, manage_calls=False)
    await event.respond(f"Promoted **{user.first_name}** in {event.chat_id}.")
  except:
    await event.reply("Seems like I don't have enough rights to do that.")
 else:
   print("#")

