from . import db
# from ..events import Cbot, Cinline
from telethon import events
from telethon.tl.types import ChannelParticipantBanned, UpdateChannelParticipant

from .. import tbot
x_b = db.betreyal

@tbot.on(events.Raw(UpdateChannelParticipant))
async def x(e):
    if not e.prev_participant:
        return
    if isinstance(e.prev_participant, ChannelParticipantBanned):
        return
    if e.channel_id == 1486931338:
        pass
    else:
        return
    if not e.new_participant:
       return
    x = (str(e)).replace("UpdateChannelParticipant", "")
    chat_id = int(str(-100) + str(e.channel_id))
    chance = 1
    prev_db = x_b.find_one({"chat_id": e.chat_id, "user_id": e.new_participant.kicked_by})
    if prev_db:
      chance = prev_db["chance"] + 1
    x_b.update_one({"chat_id": chat_id, "user_id": e.new_participant.kicked_by}, {"$set": {"chance": chance}}, upsert=True)
    if chance >= 2:
      try:
        await tbot.edit_admin(
                chat_id,
                e.new_participant.kicked_by,
                is_admin=False,
                manage_call=False,
                add_admins=False,
                pin_messages=False,
                delete_messages=False,
                ban_users=False,
                change_info=False,
                invite_users=False,
            )
      except:
        pass
    user = await tbot.get_entity(e.new_participant.kicked_by)
    chat = await tbot.get_entity(chat_id)
    x = f"""
Warning !!
  Betreyer Detected.
User: [{user.first_name}](tg://user?id={user.id})
Banned Count: {chance}
"""
    await tbot.send_message(chat_id, x)
    
