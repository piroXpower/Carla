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
 if response.status_code == 200:
    with open(path, 'wb') as file:
        for chunk in response:
            file.write(chunk)
 else:
   return await event.reply('Invalid URL Provided.')
 X = await event.reply("Uploading the screenshot...")
 await tbot.send_file(event.chat_id, path, reply_to=event.id)
 await X.delete()
 os.remove('target.jpg')
