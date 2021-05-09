from Carla import tbot, OWNER_ID
from . import can_change_info, ELITES
from Carla.events import Cbot
import os
import Carla.modules.sql.captcha_sql as sql

onn = """
Users will be asked to complete a CAPTCHA before being allowed to speak in the chat.

To change this setting, try this command again followed by one of yes/no/on/off
"""
offf = """
Users will NOT be muted when joining the chat.

To change this setting, try this command again followed by one of yes/no/on/off
"""
pos = ['on', 'y', 'yes']
neg = ['off', 'n', 'no']

@Cbot(pattern="^/captcha ?(.*)")
async def _(event):
 if event.text.startswith("!captchakick") or event.text.startswith("/captchakick") or event.text.startswith("?captchakick") or event.text.startswith("!captchakicktime") or event.text.startswith("!/captchakicktime") or event.text.startswith("?captchakicktime"):
       return
 if event.is_private:
       return #connect
 if not await can_change_info(event, event.sender_id):
       return
 settings = sql.get_mode(event.chat_id)
 args = event.pattern_match.group(1)
 if not args:
   if settings == True:
      await event.reply(onn)
   elif settings == False:
      await event.reply(offf)
 elif args in pos:
   await event.reply('CAPTCHAs have been enabled. I will now mute people when they join.')
   sql.set_mode(event.chat_id, True)
 elif args in neg:
   await event.reply('CAPTCHAs have been disabled. Users can join normally.')
   sql.set_mode(event.chat_id, False)
 else:
   await event.reply(f"That isn't a boolean - expected one of y/yes/on or n/no/off; got: {}".format(args))



 
