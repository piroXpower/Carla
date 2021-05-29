from Evelyn import tbot
from Evelyn.events import Cbot
from . import db

page = db.page

@Cbot(pattern="^/start$")
async def start(event):
 if event.is_group:
  await event.reply("Hi there, I'm online ^_^")
 elif event.is_private:
  print(6)
