from Carla import tbot, BOT_ID, OWNER_ID
import Carla.modules.sql.warns_sql as sql
from Carla.events import Cbot
from telethon import Button, events
from . import can_change_info, ELITES, is_admin, extract_time, get_user

@Cbot(pattern="^/warnlimit ?(.*)")
async def _(event):
 if event.is_private:
  return #connect
 if not await can_change_info(event, event.sender_id):
  return 
 args = event.pattern_match.group(1)
 if not args:
  settings = sql.get_limit(event.chat_id)
  await event.reply(f"Current warn limit is {settings}\n\nTo change this send the command with the new limit.")
 elif args.isdigit():
  if int(args) > 20:
   return await event.reply("Max limit is 20.\nTry lowering the limit.")
  k = sql.set_warn_limit(event.chat_id, args)
  await event.reply(f"Sucessfully updated warn limit to {args}")
 else:
  await event.reply(f"Expected an integer, got '{args}'.")
 

@Cbot(pattern="^/setwarnmode ?(.*)")
async def _(event):
 if event.is_private:
  return #connect
 if not await can_change_info(event, event.sender_id):
  return 
 args = event.pattern_match.group(1)
 if not args:
  return await event.reply("You need to specify an action to take upon too many warns. Current modes are: ban/kick/mute/tban/tmute")
 arg = args.split()
 if not arg[0] in ['ban', 'mute', 'kick', 'tban', 'tmute']:
         return await event.reply(f"Unknown type '{args}'. Please use one of: ban/kick/mute/tban/tmute")
 if arg[0] in ['tban', 'tmute']:
         if len(arg) == 1:
           return await event.reply("Looks like you're trying to set a temporary value for warnings, but haven't specified a time; use `/setwarnmode tban <timevalue>`.\nExample time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.")
         time = await extract_time(event, arg[1])
         sql.set_ban_time(event.chat_id, time)
 await event.reply(f"Updated warn mode to: {args}")
 sql.set_warn_strength(event.chat_id, str(arg[0]))
  
@Cbot(pattern="^/warn ?(.*)")
async def er(event):
 if event.text.startswith("!warns") or event.text.startswith("/warns") or event.text.startswith("?warns"):
      return
 if event.is_private:
      return
 if not await can_change_info(event, event.sender_id):
      return
 await warn_user(event)

@Cbot(pattern="^/dwarn ?(.*)")
async def er(event):
 if event.text.startswith("!dwarns") or event.text.startswith("/dwarns") or event.text.startswith("?dwarns"):
      return
 if event.is_private:
      return
 if not await can_change_info(event, event.sender_id):
      return
 if event.reply_to_msg_id:
   msg = await event.get_reply_message()
   await msg.delete()
 await warn_user(event)

async def warn_user(event):
 try:
    user, extra = await get_user(event)
 except TypeError:
    pass
 if extra:
    reason = f"\n<b>Reason:</b> {extra}"
 else:
    reason = ""
 if await is_admin(event.chat_id, user.id):
    return await event.reply("I'm not going to warn an admin!")
 limit = sql.get_limit(event.chat_id)
 num_warns, reasons = sql.warn_user(user.id, event.chat_id, reason)
 if num_warns < limit:
    text = f'User <a href="tg://user?id={user.id}">{user.first_name}</a> has been warned {num_warns}/{limit}.{reason}'
    buttons = [Button.inline("Remove warn", data=f"rm_warn-{user.id}")]
    await event.respond(text, buttons=buttons, parse_mode='html')
 else:
    print(6)


@tbot.on(events.CallbackQuery(pattern=r"rm_warn-(\d+)"))
async def rm_warn(event):
 user_id = int(event.pattern_match.group(1))
 perm = await tbot.get_permissions(event.chat_id, event.sender_id)
 if not perm.is_admin:
    return await event.answer('You need to be an admin to do this.')
 if not perm.ban_users:
    return await event.edit('You are missing the following rights to use this command: CanBanUsers.')
 await event.edit(f'<b>Warn</b> removed by <a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a>.', parse_mode='html')
 sql.remove_warn(user_id, event.chat_id)

