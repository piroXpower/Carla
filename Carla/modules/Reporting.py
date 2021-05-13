from Carla import tbot, OWNER_ID
from . import ELITES, can_change_info, get_user
from Carla.events import Cbot
from Carla.modules.sql import reporting_sql as sql
from telethon import types

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
 admins = []
 async for user in tbot.iter_participants(event.chat_id, filter=types.ChannelParticipantsAdmins):
      admins.append(user.id)
 text = "Reported <a href="tg://user?id=1743998809">RoseLoverX</a>"
 for i in admins:
     text += await get_link(i, custom_name="")
 await event.reply(text)

async def get_link(user_id, custom_name=None):
 user_name = custom_name
 return '<a href="tg://user?id={id}">{name}</a>'.format(name=user_name, id=user_id)
