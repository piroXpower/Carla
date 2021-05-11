from Carla import tbot
from Carla.events import Cbot
from Carla import CMD_LIST
from telethon import Button

string = "Contact me in PM for help!"

c_button = Button.inline("Back", data="go_back")
bl_button = Button.inline('Block
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
wlc_btn = [Button.inline("CAPTCHA", data='captcha'), Button.inline('Formatting', data='formatting')], [Button.inline('Back', data="go_back")]
antiflood = """
Antiflood

You know how sometimes, people join, send 100 messages, and ruin your chat? With antiflood, that happens no more!

Antiflood allows you to take action on users that send more than x messages in a row. Actions are: ban/kick/mute/tban/tmute

Admin commands:
- /flood: Get the current antiflood settings
- /setflood <number/off/no>: Set the number of messages after which to take action on a user. Set to '0', 'off', or 'no' to disable.
- /setfloodmode <action type>: Choose which action to take on a user who has been flooding. Options: ban/kick/mute/tban/tmute
"""


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
 elif plugin_name == 'antiflood':
   await event.reply(antiflood, buttons=c_button)
 elif plugin_name == 'blocklist' or plugin_name == 'blacklist' or plugin_name == 'blocklists' or plugin_name == 'blacklists':
   await event.reply(blocklist, buttons=c_button)
