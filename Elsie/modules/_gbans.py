from Elsie import tbot, OWNER_ID
from . import ELITES, SUDO_USERS, is_admin, get_user, db
from Elsie.events import Cbot
from telethon import Button, events
from datetime import datetime

from Elsie.modules.sql.chats_sql import get_all_chat_id 

gbanned = db.gbanned
def get_reason(id):
    return gbanned.find_one({"user": id})

Ap_chat = int(-1001273171524)
Gban_logs = int(-1001466401634)
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
Ap_req = """
(#)New Gban Request
**Originated From:** **{}** `{}`
**Sudo Admin:** [{}](tg://user?id={})
**User:** [{}](tg://user?id={})
**ID:** `{}`
**Reason:** {}
**Event Stamp:** `{}`
"""

Ap_text = """
(#)New Global Ban
**Originated From:** **{}** `{}`
**Sudo Admin:** [{}](tg://user?id={})
**User:** [{}](tg://user?id={})
**ID:** `{}`
**Reason:** {}
**Event Stamp:** `{}`
"""

Ap_update = """
(#)GBAN Update
**Originated From:** **{}** `{}`
**Sudo Admin:** [{}](tg://user?id={})
**User:** [{}](tg://user?id={})
**ID:** `{}`
**Reason:** {}
**Event Stamp:** `{}`
"""

@Cbot(pattern="^/gban ?(.*)")
async def _(event):
 global box
 if not event.sender_id == OWNER_ID and not event.sender_id in ELITES and not event.sender_id in SUDO_USERS:
   return
 if not event.reply_to_msg_id and not event.pattern_match.group(1):
   return await event.reply(b)
 user, extra = await get_user(event)
 if extra:
   reason = extra
 else:
   reason = 'None Given'
 if user.id == OWNER_ID:
     return await event.reply(e)
 elif user.id in ELITES:
     return await event.reply(d)
 elif user.id in SUDO_USERS:
     return await event.reply(c)
 if not event.sender_id == OWNER_ID:
     chats = gbanned.find({})
     for c in chats:
      if user.id == c['user']:
        to_check = get_reason(id=user.id)
        gbanned.update_one(
                {
                    "_id": to_check["_id"],
                    "bannerid": to_check["bannerid"],
                    "user": to_check["user"],
                    "reason": to_check["reason"],
                },
                {"$set": {"reason": reason, "bannerid": event.sender_id}},
            )
        await event.respond('This user is already gbanned, I am updating the reason of the gban with your reason.')
        bote = [Button.url('Appeal', 't.me/ElsieSupportChat'), Button.url('Report', 't.me/ElsieSupportChat')]
        dtext = Ap_update.format(event.chat.title, event.chat_id, event.sender.first_name, event.sender_id, user.first_name, user.id, user.id, reason, datetime.now())
        return await tbot.send_message(Gban_logs, dtext, buttons=bote)
     buttons = Button.url('Send Here', 't.me/ElsieSupportChat')
     await event.reply(a, buttons=buttons)
     bt = [Button.inline('Approve', data='agban_{}'.format(user.id)),Button.inline('Deny', data='deni')]
     dtext = Ap_text.format(event.chat.title, event.chat_id, event.sender.first_name, event.sender_id, user.first_name, user.id, user.id, reason, datetime.now())
     box = dtext
     await tbot.send_message(Ap_chat, dtext, buttons=bt)
 else:
     chats = gbanned.find({})
     for c in chats:
      if user.id == c['user']:
        to_check = get_reason(id=user.id)
        gbanned.update_one(
                {
                    "_id": to_check["_id"],
                    "bannerid": to_check["bannerid"],
                    "user": to_check["user"],
                    "reason": to_check["reason"],
                },
                {"$set": {"reason": reason, "bannerid": event.sender_id}},
            )
        await event.respond('This user is already gbanned, I am updating the reason of the gban with your reason.')
        bote = [Button.url('Appeal', 't.me/ElsieSupportChat'), Button.url('Report', 't.me/ElsieSupportChat')]
        dtext = Ap_update.format(event.chat.title, event.chat_id, event.sender.first_name, event.sender_id, user.first_name, user.id, user.id, reason, datetime.now())
        return await tbot.send_message(Gban_logs, dtext, buttons=bote)
     stre = '**⚡Snaps the Banhammer⚡**'
     await event.reply(stre)
     gbanned.insert_one(
        {"bannerid": event.sender_id, "user": user.id, "reason": reason}
    )
     dtext = Ap_text.format(event.chat.title, event.chat_id, event.sender.first_name, event.sender_id, user.first_name, user.id, user.id, reason, datetime.now())
     bote = [Button.url('Appeal', 't.me/ElsieSupportChat'), Button.url('Report', 't.me/ElsieSupportChat')]
     await tbot.send_message(Gban_logs, dtext, buttons=bote)
     cats = get_all_chat_id()
     for i in cats:
       try:
         await tbot.edit_permissions(int(i.chat_id), int(user.id), until_date=None, view_messages=False)
       except ChatAdminRequiredError:
         pass
      
 
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
    bote = [Button.url('Appeal', 't.me/ElsieSupportChat'), Button.url('Report', 't.me/ElsieSupportChat')]
    await tbot.send_message(Gban_logs, txt, buttons=bote)

