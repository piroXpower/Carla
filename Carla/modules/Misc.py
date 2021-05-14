from Carla import tbot, OWNER_ID, ubot
from Carla.events import Cbot
import requests, os, json
from . import get_user, ELITES, SUDO_USERS, can_change_info, is_admin
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from Carla.modules.sql.misc_sql import add_ad, ad_settings
from telethon import events, Button
BL = "sell buy vote ad rs btc usd netflix giveaway pornhub ss dm"

@Cbot(pattern="^/sshot ?(.*)")
async def _(event):
 BASE = 'https://render-tron.appspot.com/screenshot/'
 url = event.pattern_match.group(1)
 if not url:
   return await event.reply('Please provide the URL.')
 path = 'target.jpg'
 response = requests.get(BASE + url, stream=True)
 if not response.status_code == 200:
   return await event.reply('Invalid URL Provided.')
 else:
    X = await event.reply("Uploading the screenshot...")
    with open(path, 'wb') as file:
        for chunk in response:
            file.write(chunk)
 await tbot.send_file(event.chat_id, path, reply_to=event.id, force_document=True)
 await X.delete()
 os.remove('target.jpg')

@Cbot(pattern="^/support ?(.*)")
async def _(event):
 if event.is_private:
    return
 args = event.pattern_match.group(1)
 if not args:
   return
 await tbot.send_message(-1001273171524, f"**(#)New Request Recieved**\n**From**: [{event.sender.first_name}](tg://user?id={event.sender_id})\n\n**Request:**\n`{args}`")
 await event.reply("Sucessfully notified bot admins!")

@Cbot(pattern="^/info ?(.*)")
async def _(event):
 if not event.reply_to_msg_id and not event.pattern_match.group(1):
   user = await tbot.get_entity(event.sender_id)
 else:
  try:
   user, extra = await get_user(event)
  except TypeError:
   pass
 user_id = user.id
 first_name = user.first_name
 last_name = user.last_name
 username = user.username
 text = "╒═══「<b>User info</b>:\n"
 if first_name:
   text += f"<b>First Name:</b> {first_name}\n"
 if last_name:
   text += f"<b>Last Name:</b> {last_name}\n"
 ups = None
 if username:
   text += f"<b>Username:</b> @{username}\n"
   ups = await ubot(GetFullUserRequest(user.username))
 text += f"<b>ID:</b> <code>{user_id}</code>\n"
 text += f'<b>User link:</b> <a href="tg://user?id={user_id}">{first_name}</a>'
 if user_id == OWNER_ID:
  text += "\n\n<i>This user is my Owner</i>"
 elif user_id in ELITES:
  text += "\n\n<i>This user is one of my Devs</i>"
 elif user_id in SUDO_USERS:
  text += "\n\n<i>This user is one of my Sudo Users</i>"
 if ups:
  text += f"\n\n<b>Bio:</b> <code>{ups.about}</code>"
  text += f"\n\n<b>Gbanned: No</b>"
  text += f"\n\n╘══「 <b>Groups count:</b> {ups.common_chats_count} 」"
 else:
  text += f"\n\n╘══「 <b>Gbanned:</b> No 」"
 await event.reply(text, parse_mode='html')

@Cbot(pattern="^/bin ?(.*)")
async def bin(event):
 if event.reply_to_msg_id:
   msg = await event.get_reply_message()
   bin = msg.text
 elif event.pattern_match.group(1):
   bin = event.pattern_match.group(1)
 else:
   return await event.reply("Enter the bin to get info.")
 url = "https://lookup.binlist.net/{}"
 response = requests.request("GET", url.format(bin))
 k = json.load(response.text)
 emoji = k["country"]["emoji"]
 text = f"BIN/IIN: `{bin}`{emoji}"
 if k["scheme"]:
   scheme = k["scheme"]
   text += f"\nCard Brand: <b>{scheme}</b>"
 await event.respond(text, parse_mode='htm')


@Cbot(pattern="^/antiads ?(.*)")
async def aa(event):
 pro = ['y', 'yes', 'on']
 noob = ['n', 'no', 'off']
 if event.is_private:
    return
 if not await can_change_info(event, event.sender_id):
    return
 args = event.pattern_match.group(1)
 if not args:
    mode = ad_settings(event.chat_id)
    await event.reply(f"Current Ad filter settings is : **__{mode}__**")
 elif args in pro:
    add_ad(event.chat_id, True)
    await event.reply("**Enabled** Ad filtering for this chat.")
 elif args in noob:
    add_ad(event.chat_id, False)
    await event.reply("**Disabled** Ad filtering for this chat.")
 else:
    await event.reply(f"`{args}` is not recognised as a valid input. Try one of y/yes/on/n/no/off.")

@tbot.on(events.NewMessage(pattern=None))
async def h(event):
 if event.is_private:
   return
 if not ad_settings(event.chat_id):
   return
 if await is_admin(event.chat_id, event.sender_id):
   return
 text = (event.text).lower()
 match = 0
 Blist = BL.split(' ')
 for i in Blist:
   if i in str(text):
     match += 1
 if match >= 4:
     await event.delete()
 elif match >= 3 and event.fwd_from:
     await event.delete()
 elif match >= 3 and len(text) >= 45:
     await event.delete()

#soon
