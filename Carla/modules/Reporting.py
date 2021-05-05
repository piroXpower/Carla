from Carla import tbot, OWNER_ID
from . import ELITES, can_change_info, get_user
from Carla.events import Cbot
from Carla.modules.sql import reporting_sql as sql

Ron = """
Reports are currently enabled in this chat.
Users can use the /report command, or mention @admin, to tag all admins.

To change this setting, try this command again, with one of the following args: yes/no/on/off
"""
Roff = """
Reports are currently disabled in this chat.

To change this setting, try this command again, with one of the following args: yes/no/on/off
"""

@Cbot(pattern="^/reports ?(.*)")
async def _(event):
 if event.is_private:
    return #connect
 if not event.sender_id == OWNER_ID or event.sender_id in ELITES:
   k = await can_change_info(event, event.sender_id)
   if not k:
     return
 args = event.pattern_match.group(1)
 chat = event.chat_id
 if args:
        if args == "on" or args == "yes":
            await event.reply("Users will now be able to report messages.")
            sql.set_chat_setting(chat, True)
        elif args == "off" or args == "no":
            await event.reply("Users will no longer be able to report via @admin or /report.")
            sql.set_chat_setting(chat, False)
        else:
            await event.reply("Your input was not recognised as one of: yes/no/on/off")
            return
 else:
  if sql.chat_should_report(chat):
    await event.reply(Ron)
  else:
    await event.reply(Roff)

@Cbot(pattern="^/report ?(.*)")
async def _(event):
 if event.is_private:
  return #add_reply
 if await is_admin(event.chat_id, event.sender_id):
      return
 r_msg = None
 if event.reply_to_msg_id:
    msg = await event.get_reply_message()
    if await is_admin(event.chat_id, msg.sender_id):
           return await event.reply("Silly you can't report an admin!")
    r_msg = msg.id
    text = f"Reported [{msg.sender.first_name}](tg://user?id={msg.sender_id})."
 elif event.pattern_match.group(1):
  try:
   user, extra = await get_user(event)
  except TypeError:
   pass
  text = f"Reported [{user.first_name}](tg://user?id={user.sender_id})."
 else:
  text = "Reported to admins.​​​​"
 await event.respond(text, reply_to=r_msg)
      
