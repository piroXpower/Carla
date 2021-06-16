import .mongodb.notes_db as db
from . import can_change_info
from Evelyn.events import Cbot

@Cbot(pattern="^/save ?(.*)")
async def save(event):
 if event.is_private:
   return
 if event.from_id:
   if event.is_group:
     if not await can_change_info(event, event.sender_id):
       return
   if not event.reply_to and not event.pattern_match.group(1):
       return await event.reply("You need to give the note a name!")
   elif event.reply_to:
       n = event.pattern_match.group(1)
       r_msg = await event.get_reply_messages()
       if r_msg.media:
          file_id, access_hash, file_reference = file_ids_gather(r_msg)
       if not r_msg.text and not r_msg.media:
          return await event.reply("you need to give the note some content!")
       if not n:
          return await event.reply("You need to give the note a name!")
       if r_msg.reply_markup:
          _buttons = get_reply_msg_btns_text(r_msg)
          r_note = r_msg.text + _buttons
   elif event.pattern_match.group(1):
      n = event.pattern_match.group(1)
      n = n.split(None, 1)
      if len(n) == 1:
        return await event.reply("you need to give the note some content!")
      n = n[0]
      r_note = n[1]
   db.save_note(event.chat_id, n, r_note)
   await event.reply(f"Saved note `{n}`")


       
