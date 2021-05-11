from Carla import tbot
from Carla.events import Cbot
from Carla import CMD_LIST
from telethon import Button

string = "Contact me in PM for help!"

welcome = """
Greetings

Give your members a warm welcome with the greetings module! Or a sad goodbye... Depends!

Admin commands:
- /welcome <yes/no/on/off>: Enable/disable welcomes messages.
- /goodbye <yes/no/on/off>: Enable/disable goodbye messages.
- /setwelcome <text>: Set a new welcome message. Supports markdown, buttons, and fillings.
- /resetwelcome: Reset the welcome message.
- /setgoodbye <text>: Set a new goodbye message. Supports markdown, buttons, and fillings.
- /resetgoodbye: Reset the goodbye message.
- /cleanservice <yes/no/on/off>: Delete all service messages. Those are the annoying 'x joined the group' notifications you see when people join.
- /cleanwelcome <yes/no/on/off>: Delete old welcome messages. When a new person joins, or after 5 minutes, the previous message will get deleted.

Examples:
- Get the welcome message without any formatting
-> /welcome noformat
"""
wlc_btn = [Button.inline("CAPTCHA", data='captcha'), Button.inline('Formatting', data='formatting')], Button.inline('Back', data="go_back")


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
   await event.reply(welcome, buttons=wlc_btn)
