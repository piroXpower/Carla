from Carla import tbot
from Carla.events import Cbot
from Carla import CMD_LIST
from telethon import Button

string = "Contact me in PM for help!"
buttons = Button.url("Click me for help", "t.me/MissCarla_bot?start=help_{}")

@Cbot(pattern="^/help ?(.*)")
async def help(event):
 if not event.is_private:
  if event.pattern_match.group(1):
    module = event.pattern_match.group(1)
  else:
    module = "all"
  await event.reply(string, buttons=buttons.format(module))

@Cbot(pattern="^/start help_(.*)")
async def hh(event):
 module = event.pattern_match.group(1)
 await event.reply(str(module))
