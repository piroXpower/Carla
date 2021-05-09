from Carla import tbot
from Carla.events import Cbot
import requests, os
from . import get_user

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
 await tbot.send_file(event.chat_id, path, reply_to=event.id)
 await X.delete()
 os.remove('target.jpg')

@Cbot(pattern="^/request ?(.*)")
async def _(event):
 if not event.is_private:
    return
 args = event.pattern_match.group(1)
 if not args:
   return await event.respond('Include some text in request.')
 await tbot.send_message(-1001273171524, f"**(#)New Request Recieved**\n**From**: [{event.sender.first_name}](tg://user?id={event.sender_id})\n\n**Request:**\n`{args}`")
 await event.respond("Sucessfully notified admins!")

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
 text = "<b>User Information:</b>\n"
 text += f"<b>ID:</b> <code>{user_id}</code>\n"
 if first_name:
   text += f"<b>First Name:</b> {first_name}\n"
 if last_name:
   text += f"<b>Last Name:</b> {last_name}\n"
 if username:
   text += f"<b>Username:</b> @{username}\n"
 text += f'<b>User link:</b> <a href="tg://user?id={user_id}">{first_name}</a>'
 await event.reply(text, parse_mode="html")
 
