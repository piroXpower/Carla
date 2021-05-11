from Carla import tbot
from Carla.events import Cbot
from . import can_change_info
import Carla.modules.sql.notes_sql as sql
from telethon import events, Button


@Cbot(pattern="^/save ?(.*)")
async def save(event):
  if event.is_private:
    return
  if not await can_change_info(event, event.sender_id):
    return
  if not event.reply_to_msg_id and not event.pattern_match.group(1):
    return await event.reply("You need to give the note a name!")
  elif event.reply_to_msg_id:
    if not event.pattern_match.group(1):
      return await event.reply("You need to give the note a name!")
    msg = await event.get_reply_message()
    if msg.media:
      file = msg.file.id
      note = None
    else:
      note = msg.message
      file = None
    keyword = event.pattern_match.group(1)
  elif not event.reply_to_msg_id and event.pattern_match.group(1):
    file = None
    args = event.pattern_match.group(1)
    args = args.split(" ", 1)
    if len(args) == 1:
      return await event.reply("You need to give the note some content!")
    keyword = args[0]
    note = args[1]
  p = sql.add_note(event.chat_id, keyword, note, file)
  if p:
    await event.reply(f"Saved note '{keyword}'.")
    
    
  
