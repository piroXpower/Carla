from Carla import tbot
from Carla.events import Cbot
import requests, os

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
 await tbot.send_message(-1001273171524, f"**New Request Recieved**\nSend BY: [{event.sender.first_name}](tg://user?id={event.sender_id})\n\n**Request:**\n{args}")
