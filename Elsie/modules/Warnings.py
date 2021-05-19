from Elsie import tbot, BOT_ID, OWNER_ID
import Elsie.modules.sql.warns_sql as sql
from Elsie.events import Cbot
from telethon import Button, events
import time
from . import can_change_info, ELITES, is_admin, extract_time, get_user, g_time

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
 cr = time.time()
 try:
    user, extra = await get_user(event)
 except TypeError:
    pass
 if extra:
    reason = f"\n<b>Reason:</b> {extra}"
 else:
    reason = ""
 limit = sql.get_limit(event.chat_id)
 num_warns, reasons = sql.warn_user(user.id, event.chat_id, reason)
 if num_warns < limit:
    text = f'User <a href="tg://user?id={user.id}">{user.first_name}</a> has been warned {num_warns}/{limit}.{reason}'
    buttons = [Button.inline("Remove warn", data=f"rm_warn-{user.id}")]
    await event.respond(text, buttons=buttons, parse_mode='html')
 else:
    tt = 0
    mode = sql.get_warn_strength(event.chat_id)
    if mode in ['tban', 'tmute']:
       tt = sql.get_ban_time(event.chat_id)
    sql.reset_warns(user.id, event.chat_id)
    await excecute_warn(event, user.id, user.first_name, mode, reason, tt, limit)
 kek = time.time() - cr
 await event.respond(str(kek))

async def excecute_warn(event, user_id, name, mode, reason="", tt=0, limit=3):
           if mode == 'ban':
                 await tbot.edit_permissions(event.chat_id, user_id, until_date=None, view_messages=False)
                 if reason:
                     reason = f"\nReason: <i>{reason}</i>"
                 await event.respond(f'Thats <b>{limit}/{limit}</b> Warnings, <a href="tg://user?id={user_id}">{name}</a> Has been <b>Banned!</b>{reason}', parse_mode='html')
           elif mode == 'kick':
                 await tbot.kick_participant(event.chat_id, event.sender_id)
                 if reason:
                     reason = f"\nReason: <i>{reason}</i>"
                 await event.respond(f'Thats <b>{limit}/{limit}</b> Warnings, <a href="tg://user?id={user_id}">{name}</a> has been <b>Kicked!</b>{reason}', parse_mode='html')
           elif mode == 'mute':
                 await tbot.edit_permissions(event.chat_id, event.sender_id, until_date=None, send_messages=False)
                 if reason:
                     reason = f"\nReason: <i>{reason}</i>"
                 await event.respond(f'Thats <b>{limit}/{limit}</b> Warnings, <a href="tg://user?id={user_id}">{name}</a> has been <b>Muted!</b>{reason}', parse_mode='html')
           elif mode == 'tban':
                 if reason:
                     reason = f"\nReason: <i>{reason}</i>"
                 tt = g_time(tt)
                 await event.respond(f'Thats <b>{limit}/{limit}</b> Warnings, <a href="tg://user?id={user_id}">{name}</a> has been Banned for <b>{tt}</b>!{reason}', parse_mode='html')
                 await tbot.edit_permissions(event.chat_id, event.sender_id, until_date=time.time() + int(tt), view_messages=False)
           elif mode == 'tmute':
                 if reason:
                     reason = f"\nReason: <i>{reason}</i>"
                 tt = g_time(tt)
                 await event.respond(f'Thats <b>{limit}/{limit}</b> Warnings, <a href="tg://user?id={user_id}">{name}</a> has been Muted for <b>{tt}</b>!{reason}', parse_mode='html')
                 await tbot.edit_permissions(event.chat_id, event.sender_id, until_date=time.time() + int(tt), send_messages=False)

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

@Cbot(pattern="^/rmwarn ?(.*)")
async def le(event):
 if event.is_private:
      return
 if not await can_change_info(event, event.sender_id):
      return
 user = None
 reason = ""
 try:
   user, reason = await get_user(event)
 except TypeError:
   pass
 if not user:
   return
 if reason:
   reason = "\n<b>Reason:</b> {reason}"
 result = sql.get_warns(user.id, event.chat_id)
 if result and result[0] in [0, False]:
   return await event.reply("User <a href='tg://user?id={user_id}'>{first_name}</a> has no Warnings.", parse_mode='htm')
 user_id = user.id
 chat_id = event.chat_id
 first_name = user.first_name
 text = f"Removed <a href='tg://user?id={user_id}'>{first_name}</a>'s last warn.{reason}"
 await event.reply(text, parse_mode='htm')
 sql.remove_warn(user_id, chat_id)



 
