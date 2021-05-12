from Carla import tbot
from Carla.events import Cbot
from . import can_change_info, db, is_admin
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
      note = msg.text
    else:
      note = msg.text
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
  try:
    sql.add_note(event.chat_id, keyword, note, file)
  except Exception as e:
    await event.respond(str(e))
  await event.reply(f"Saved note '{keyword}'.")
    
@tbot.on(events.NewMessage(pattern=r"\#(\S+)"))
async def nt(event):
  name = event.pattern_match.group(1)
  if not name:
    return
  note = sql.get_notes(event.chat_id, name)
  if not note:
    return
  reply_w = note.reply
  if "{admin}" in note.reply:
   reply_w = note.reply.replace("{admin}", "")
   if not await is_admin(event.chat_id, event.sender_id):
      return
  if note.file:
    await event.reply(reply_w, file=note.file)
  else:
    await event.reply(reply_w

@Cbot(pattern="^/get ?(.*)")
async def getnote(event):
 name = event.pattern_match.group(1)
 if not name:
   return await event.reply("Not enough arguments!")
 note = sql.get_notes(event.chat_id, name)
 if not note:
   return await event.reply("Note not found.")
 reply_w = note.reply
 if "{admin}" in note.reply:
   reply_w = note.reply.replace("{admin}", "")
   if not await is_admin(event.chat_id, event.sender_id):
      return
 if note.file:
    await event.reply(reply_w, file=note.file)
 else:
    await event.reply(reply_w)
