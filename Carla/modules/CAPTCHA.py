from Carla import tbot, OWNER_ID
from . import can_change_info, ELITES
from Carla.events import Cbot
import os
import Carla.modules.sql.captcha_sql as SQL

onn = """
Users will be asked to complete a CAPTCHA before being allowed to speak in the chat.

To change this setting, try this command again followed by one of yes/no/on/off
"""
offf = """
Users will NOT be muted when joining the chat.

To change this setting, try this command again followed by one of yes/no/on/off
"""

@Cbot(pattern="^/captcha ?(.*)")
async def _(event):
 if event.text.startswith("!captchakick") or event.text.startswith("/captchakick") or. event.text.startswith("?captchakick") or event.text.startswith("!captchakicktime") or event.text.startswith("!/captchakicktime") or event.text.startswith("?captchakicktime"):
       return
 if event.is_private:
       return #connect
 if not await can_change_info(event, event.sender_id):
       return
 settings = get_mode(event.chat_id)
 args = event.pattern_match.group(1)
 if not args:
   if settings == True:
      await event.reply(onn)
   elif settings == False:
      await event.reply(offf)
 
