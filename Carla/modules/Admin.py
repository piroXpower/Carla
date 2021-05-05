from Carla import tbot, OWNER_ID
from Carla.events import Cbot
from . import ELITES, cb_can_promote_users, can_promote_users, get_user, is_admin
from telethon import Button, events

btext = "It looks like you're anonymous. Tap this button to confirm your identity."

@Cbot(pattern="^/promote ?(.*)")
async def _(event):
 if event.is_private:
  return #connection
 if event.from_id:
  title = None
  if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
   await can_promote_users(event.chat_id, event.sender_id)
  try:
   user, title = await get_user(event)
  except:
   pass
  if not title:
    title = "Admin"
  if await is_admin(event.chat_id, user.id):
    return await event.reply("This User is already an Admin!")
  try:
    await tbot.edit_admin(event.chat_id, user.id, manage_call=False, add_admins=False, pin_messages=True, delete_messages=True, ban_users=True, change_info=True, invite_users=True, title=title) 
    await event.respond(f"Promoted **{user.first_name}** in **{event.chat.title}**.")
  except:
    await event.reply("Seems like I don't have enough rights to do that.")
 else:
   await anonymous(event, 'promote')

@Cbot(pattern="^/superpromote ?(.*)")
async def _(event):
 if event.is_private:
  return #connection
 title = None
 if event.from_id:
  if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
   await can_promote_users(event.chat_id, event.sender_id)
  try:
   user, title = await get_user(event)
  except:
   pass
  if not title:
    title = "Admin"
  if await is_admin(event.chat_id, user.id):
    return await event.reply("This User is already an Admin!")
  try:
    await tbot.edit_admin(event.chat_id, user.id, manage_call=True, add_admins=True, pin_messages=True, delete_messages=True, ban_users=True, change_info=True, invite_users=True, title=title) 
    await event.respond(f"Promoted **{user.first_name}** in **{event.chat.title}** with full Rights.")
  except:
    await event.reply("Seems like I don't have enough rights to do that.")
 else:
   await anonymous(event, 'superpromote')

@Cbot(pattern="^/demote ?(.*)")
async def _(event):
 if event.is_private:
  return #connection
 if event.from_id:
  if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
   await can_promote_users(event.chat_id, event.sender_id)
  try:
   user, title = await get_user(event)
  except:
   pass
  if user.bot:
   return await event.reply("Due to telegram limitations, I can't demote bots. Please demote them manually!")
  if not await is_admin(event.chat_id, user.id):
    return await event.reply("This User is not an Admin!")
  try:
    await tbot.edit_admin(event.chat_id, user.id, is_admin=False, manage_call=False, add_admins=False, pin_messages=False, delete_messages=False, ban_users=False, change_info=False, invite_users=False) 
    await event.respond(f"Demoted **{user.first_name}**.")
  except:
    await event.reply("Seems like I don't have enough rights to do that.")
 else:
   await anonymous(event, 'demote')

async def anonymous(event, mode):
  try:
   user, title = await get_user(event)
  except:
   pass
  if user.bot and mode == 'demote':
   return await event.reply("Due to telegram limitations, I can't demote bots. Please demote them manually!")
  data = f"{user.id}!{mode}"
  buttons = Button.inline("Click to prove Admin", data="sup_{}".format(data))
  await event.reply(btext, buttons=buttons)

@tbot.on(events.CallbackQuery(pattern=r"sup(\_(.*))"))
async def _(event):
 title = None
 tata = event.pattern_match.group(1)
 data = tata.decode()
 input = data.split("_", 1)[1]
 user_id, mode = input.split("!", 1)
 user_id = user_id.strip()
 mode = mode.strip()
 await cb_can_promote_users(event.chat_id, event.sender_id)
 if mode == 'promote':
  try:
    await tbot.edit_admin(event.chat_id, int(user_id), manage_call=False, add_admins=False, pin_messages=True, delete_messages=True, ban_users=True, change_info=True, invite_users=True, title="Admin") 
    text = f"Promoted **User** in **{event.chat.title}**."
  except:
    text = "Seems like I don't have enough rights to do that."
 elif mode == 'superpromote':
  try:
    await tbot.edit_admin(event.chat_id, int(user_id), manage_call=True, add_admins=True, pin_messages=True, delete_messages=True, ban_users=True, change_info=True, invite_users=True, title="Admin") 
    text = f"Promoted **User** in **{event.chat.title}** with full Rights."
  except:
    text = "Seems like I don't have enough rights to do that."
 elif mode == 'demote':
  try:
    await tbot.edit_admin(event.chat_id, int(user_id), is_admin=False, manage_call=False, add_admins=False, pin_messages=False, delete_messages=False, ban_users=False, change_info=False, invite_users=False) 
    text = "Demoted!."
  except:
    text = "Seems like I don't have enough rights to do that."
 await event.edit(text)
