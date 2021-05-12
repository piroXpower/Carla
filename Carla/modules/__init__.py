from Carla import tbot, MONGO_DB_URI, BOT_ID
from telethon import events, Button
import time, re
from pymongo import MongoClient
from Carla.modules.sql.chats_sql import is_chat, add_chat

SUDO_USERS = []
ELITES = []

#DB
client = MongoClient(MONGO_DB_URI)
db = client["Rylee"]

#Add chat to DB
@tbot.on(events.ChatAction)
async def handler(event):
    if event.user_added:
        if event.user_id == BOT_ID:
           if not is_chat(event.chat_id):
                add_chat(event.chat_id)

async def can_promote_users(event, user_id):
 perm = await tbot.get_permissions(event.chat_id, user_id)
 if not perm.is_admin:
  await event.reply("You need to be an admin to do this.")
  return False
 if not perm.add_admins:
  await event.reply("You are missing the following rights to use this command: CanPromoteUsers.")
  return False
 return True

async def cb_can_promote_users(event, user_id):
 perm = await tbot.get_permissions(event.chat_id, user_id)
 if not perm.is_admin:
  await event.answer("You need to be an admin to do this.")
  return False
 if not perm.add_admins:
  await event.edit("You are missing the following rights to use this command: CanPromoteUsers.")
  return False
 return True

async def can_change_info(event, user_id):
 perm = await tbot.get_permissions(event.chat_id, user_id)
 if not perm.is_admin:
  await event.reply("You need to be an admin to do this.")
  return False
 if not perm.change_info:
  await event.reply("You are missing the following rights to use this command: CanChangeInfo.")
  return False
 return True

async def can_pin_messages(event, user_id):
 perm = await tbot.get_permissions(event.chat_id, user_id)
 if not perm.is_admin:
  await event.reply("You need to be an admin to do this.")
  return False
 if not perm.pin_messages:
  await event.reply("You are missing the following rights to use this command: CanPinMessages.")
  return False
 return True

async def can_ban_users(event, user_id):
 perm = await tbot.get_permissions(event.chat_id, user_id)
 if not perm.is_admin:
  await event.reply("You need to be an admin to do this.")
  return False
 if not perm.ban_users:
  await event.reply("You are missing the following rights to use this command: CanBanUsers.")
  return False
 return True

async def is_owner(event, user_id):
 perm = await tbot.get_permissions(event.chat_id, user_id)
 if not perm.is_admin:
  await event.reply("You need to be an admin to do this.")
  return False
 if not perm.is_creator:
  await event.reply("You need to be the chat Creator to do this!")
  return False
 return True

async def is_admin(chat_id, user):
 try:
    sed = await tbot.get_permissions(chat_id, user)
    if sed.is_admin:
          is_mod = True
    else:
          is_mod = False
 except:
    is_mod = False
 return is_mod

async def get_user(event):
    args = event.pattern_match.group(1).split(" ", 1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await tbot.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        extra = None
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.reply("I don't know who you're talking about, you're going to need to specify a user...!")
            return
        try:
            user_obj = await tbot.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return

    return user_obj, extra

async def extract_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await message.reply("Invalid time amount specified.")
            return ""
        if unit == "m":
            bantime = int(time_num) * 60
        elif unit == "h":
            bantime = int(time_num) * 60 * 60
        elif unit == "d":
            bantime = int(time_num) * 24 * 60 * 60
        else:
            return 
        return bantime
    else:
        await message.reply(
            "Invalid time type specified. Expected m,h, or d, got: {}".format(
                time_val[-1]
            )
        )
        return False


def g_time(time):
 time = int(time)
 if time >= 86400:
   time = time/(60*60*24)
   text = f'{int(time)} days'
   if not time - int(time) == 0:
     kuk = (time - int(time))*24
     text += f' {int(kuk)} hours'
 elif time >= 3600 < 86400:
   time = time/(60*60)
   text = f'{int(time)} hours'
   if not time - int(time) == 0:
     kuk = (time - int(time))*60
     text += f' {int(kuk)} minutes'
 elif time >= 60 < 3600:
   time = time/60
   text = f'{int(time)} minutes'
   if not time - int(time) == 0:
     kuk = (time - int(time))*60
     text += f' {int(kuk)} seconds'
 return text


def gen_button_from_text(text):
 total = []
 buttons = text.split("|", 1)[1]
 if "•" in buttons:
   buttons = buttons.split("•")
   lbutton = []
   for i in buttons:
     params = re.findall(r"\'(.*?)\'", i) or re.findall(
                                r"\"(.*?)\"", i
                            )
     if "[" and "]" in i:
       lbutton.append([params])
     else:
       lbutton.append(params)
   butto = []
   new = []
   for i in lbutton:
      if len(i) == 1:
        for j in i:
          i = j
          new.append(Button.url(*i))
          if len(new) == 1:
             total.append(new)
             new = []
      else:
        butto.append(Button.url(*i))
        if len(butto) == 3:
           total.append(butto)
           butto = []
 total.append(butto)
 return total

def kek(text):
 total = []
 buttons = text.split("|", 1)[1]
 if "•" in buttons:
   buttons = buttons.split("•")
   lbutton = []
   nbutton = []
   for i in buttons:
     params = re.findall(r"\'(.*?)\'", i) or re.findall(
                                r"\"(.*?)\"", i
                            )
     new = []
     same =[]
     if "[" and "]" in i:
       nbutton.append([params])
     else:
       lbutton.append(params)
     
 return nbutton.append(lbutton)

def get_markup(reply_markup):
  btn = ""
  for i in reply_markup.rows:
    for k in i.buttons:
      text = k.text
      url = k.url
      final = f"'{text}', '{url}'"
      button += final
  return button
