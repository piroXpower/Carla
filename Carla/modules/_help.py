from Carla import tbot
from Carla.events import Cbot
from Carla import CMD_LIST
from telethon import Button

string = "Contact me in PM for help!"

@Cbot(pattern="^/help ?(.*)")
async def help(event):
 if not event.is_private:
  if event.pattern_match.group(1):
    module = event.pattern_match.group(1)
  else:
    module = "all"
  buttons = Button.url("Click me for help", "t.me/MissCarla_bot?start=help_{}".format(module))
  await event.reply(string, buttons=buttons)

@Cbot(pattern="^/start help_(.*)")
async def hh(event):
 plugin_name = (event.pattern_match.group(1)).lower()
 if plugin_name == 'welcome':
   await event.reply("Son")
