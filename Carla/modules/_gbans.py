from Carla import tbot, OWNER_ID
from . import ELITES, SUDO_USERS, is_admin, get_user, db
from Carla.events import Cbot
from telethon import Button

gbanned = db.gbanned
def get_reason(id):
    return gbanned.find_one({"user": id})

Ap_chat = -1001326741686

#Constants
a = """
__Your request sent to DEVS waiting for approval. Till that send proofs to DEVS.__
"""
b = """
You don't seem to be referring to a user or the ID specified is incorrect..
"""
c = """
Fool! You can't ban this user. noob!🤭
"""
d = """
Fool! You can't ban my developer. noob!🤣
"""
e = """
Fool! You can't ban my master. noob!😑
"""

@Cbot(pattern="^/gban ?(.*)")
async def _(event):
 if not event.sender_id == OWNER_ID and not event.sender_id in ELITES and not event.sender_id in SUDO_USERS:
   return
 if not event.reply_to_msg_id and not event.pattern_match.group(1):
   return await event.reply(b)
 user, extra = await get_user(event)
 if user.id == OWNER_ID:
     return await event.reply(e)
 elif user.id in ELITES:
     return await event.reply(d)
 elif user.id in SUDO_USERS:
     return await event.reply(c)
 if event.sender_id == OWNER_ID:
     buttons = Button.url('Send Here', 't.me/lunatestgroup')
     await event.reply(a, buttons=buttons)
 
