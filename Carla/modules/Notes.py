from Carla import tbot
from Carla.events import Cbot
from . import can_change_info, db, is_admin, gen_button_from_text, get_markup
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
      if msg.reply_markup:
        finale = get_markup(msg.reply_markup)
        note += "|"
        note += finale
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
    return await event.respond(str(e))
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
 reply_w = reply_w.replace("{noprivate}", "")
 reply_w = reply_w.replace("{admin}", "")
 reply_w = reply_w.replace("{private}", "")
 if "{admin}" in note.reply:
   if not await is_admin(event.chat_id, event.sender_id):
      return await event.reply("This note is for admins only.")
 butto = None
 if '|' in note.reply:
   reply_w, butto = gen_button_from_text(note.reply)
 mode = sql.get_mode(event.chat_id)
 if mode == False or "{noprivate}" in note.reply:
  if note.file:
    try:
     await event.reply(reply_w, file=note.file, buttons=butto)
    except:
     await event.reply(reply_w, file=note.file)
  else:
    try:
     await event.reply(reply_w, buttons=butto)
    except:
     await event.reply(reply_w)
 elif mode == True or "{private}" in note.reply:
    text = f"Tap here to view '{name}' in your private chat."
    luv = f"{event.chat_id}_{name}"
    buttons = Button.url("Click me!", "t.me/MissCarla_bot?start=notes_{}".format(luv))
    await event.reply(text, buttons=buttons)

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
      return await event.reply("This note is for admins only.")
 mode = sql.get_mode(event.chat_id)
 if mode == False:
  if note.file:
    await event.reply(reply_w, file=note.file)
  else:
    await event.reply(reply_w)
 elif mode == True:
    text = f"Tap here to view '{name}' in your private chat."
    luv = f"{event.chat_id}_{name}"
    buttons = Button.url("Click me!", "t.me/MissCarla_bot?start=notes_{}".format(luv))
    await event.reply(text, buttons=buttons)

pos = ['y', 'yes', 'on']
neg = ['n', 'no', 'off']

@Cbot(pattern="^/privatenotes ?(.*)")
async def pn(event):
 if event.is_private:
   return #conn
 if not await can_change_info(event, event.sender_id):
   return
 args = event.pattern_match.group(1)
 if not args:
  mode = sql.get_mode(event.chat_id)
  if mode == False:
      await event.reply("Your notes are currently being sent in the group.")
  else:
      await event.reply("Your notes are currently being sent in private. Carla will send a small note with a button which redirects to a private chat.")
 elif args in pos:
   await event.reply("Carla will now send a message to your chat with a button redirecting to PM, where the user will receive the note.")
   sql.set_mode(event.chat_id, True)
 elif args in neg:
   await event.reply("Carla will now send notes straight to the group.")
   sql.set_mode(event.chat_id, False)
 else:
   await event.reply(f"failed to get boolean value from input: expected one of y/yes/on or n/no/off; got: {args}")

@Cbot(pattern="^/start notes_(.*)")
async def kp(event):
 name = event.pattern_match.group(1)
 chat, name = name.split("_", 1)
 chat = int(chat.strip())
 name = name.strip()
 note = sql.get_notes(chat, name)
 if not note:
   return
 reply_w = note.reply
 if '|' in note.reply:
   reply_w, butto = gen_button_from_text(note.reply)
 if note.file:
    try:
     await event.reply(reply_w, file=note.file, buttons=butto)
    except:
     await event.reply(reply_w, file=note.file)
 else:
    try:
     await event.reply(f"**{name}:**\n\n" + reply_w, buttons=butto)
    except:
     await event.reply(f"**{name}:**\n\n" + reply_w)

@Cbot(pattern="^/notes")
async def bin(event):
 if event.is_private:
   return
 print(6)

#soon
