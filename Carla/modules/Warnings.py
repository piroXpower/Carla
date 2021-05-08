from Carla import tbot, BOT_ID, OWNER_ID
import Carla.modules.sql.warns_sql as sql
from Carla.events import Cbot
from telethon import Button, events
from . import can_change_info, ELITES, is_admin, extract_time

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
         o = sql.set_ban_time(event.chat_id, time)
         if not o:
             return
 await event.reply(f"Updated warn mode to: {lol}")
 sql.set_warn_strength(event.chat_id, str(arg[0]))
  
         
