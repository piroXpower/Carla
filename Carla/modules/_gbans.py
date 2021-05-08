from Carla import tbot, OWNER_ID
from . import ELITES, SUDO_USERS, is_admin, get_user, db
from Carla.events import Cbot
from telethon import Button, events
from datetime import datetime

gbanned = db.gbanned
def get_reason(id):
    return gbanned.find_one({"user": id})

Ap_chat = int(-1001326741686)
Gban_logs = int(-1001398201585)
box = None

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
Ap_text = """
#New Gban Request
Originated From: **{}** `{}`
Sudo Admin: [{}](tg://user?id={})
User: [{}](tg://user?id={})
ID: `{}`
Event Stamp: `{}`
"""

@Cbot(pattern="^/gban ?(.*)")
async def _(event):
 global box
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
     bt = [Button.inline('Approve', data='agban_{}'.format(user.id)),Button.inline('Deny', data='deni')]
     dtext = Ap_text.format(event.chat.title, event.chat_id, event.sender.first_name, event.sender_id, user.first_name, user.id, user.id, datetime.now())
     box = dtext
     await tbot.send_message(Ap_chat, dtext, buttons=bt)

@tbot.on(events.CallbackQuery(pattern=r"agban(\_(.*))"))
async def delete_fed(event):
    global box
    tata = event.pattern_match.group(1)
    data = tata.decode()
    user_id = data.split("_", 1)[1]
    user_id = int(user_id)
    await event.edit(buttons=None)
    await event.respond(f'Request approved by {event.sender.first_name}')
    txt = f"**Approved By:** [{event.sender.first_name}](tg://user?id={event.sender_id}){box}"
    txt = txt.replace('request', '')
    await tbot.send_message(Gban_logs, txt)
