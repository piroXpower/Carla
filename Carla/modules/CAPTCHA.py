from Carla import tbot, OWNER_ID
from . import can_change_info, ELITES, extract_time, g_time
from Carla.events import Cbot
import os
import Carla.modules.sql.captcha_sql as sql
import Carla.modules.sql.welcome_sql as cas


onn = """
Users will be asked to complete a CAPTCHA before being allowed to speak in the chat.

To change this setting, try this command again followed by one of yes/no/on/off
"""
offf = """
Users will NOT be muted when joining the chat.

To change this setting, try this command again followed by one of yes/no/on/off
"""
ca_on = """
I am currently kicking users that haven't completed the CAPTCHA after {}.

To change this setting, try this command again followed by one of yes/no/on/off
"""
ca_off = """
Users that don't complete their CAPTCHA are allowed to stay in the chat, muted, and can complete the CAPTCHA whenever.

To change this setting, try this command again followed by one of yes/no/on/off
"""
smdd = """
Users will stay muted until they use the CAPTCHA.

To change the CAPTCHA mute time, try this command again with a time value.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""
sudd = """
If users haven't unmuted themselves after {}, they will be unmuted automatically.

To change the CAPTCHA mute time, try this command again with a time value.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""
ca_ot = """
Users that don't complete their CAPTCHA are allowed to stay in the chat, muted, and can complete the CAPTCHA whenever.

To change the CAPTCHA kick time, try this command again with a time value.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""
ca_time = """
I am currently kicking users that haven't completed the CAPTCHA after {}.

To change the CAPTCHA kick time, try this command again with a time value.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""
caut = """
That isn't a valid time - '{}' does not follow the expected time patterns.
Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
"""
bu_h = """
The current CAPTCHA mode is: button
Button CAPTCHAs simply require a user to press a button in their welcome message to confirm they're human.

Available CAPTCHA modes are: button/math/text
"""
tx_h = """
The current CAPTCHA mode is: text
Text CAPTCHAs require the user to answer a CAPTCHA containing letters and numbers.

Available CAPTCHA modes are: button/math/text
"""
mt_h = """
The current CAPTCHA mode is: math
Math CAPTCHAs require the user to solve a basic maths question. Please note that this may discriminate against users with little maths knowledge.

Available CAPTCHA modes are: button/math/text
"""


pos = ['on', 'y', 'yes']
neg = ['off', 'n', 'no']

@Cbot(pattern="^/captcha ?(.*)")
async def _(event):
 if event.text.startswith("!captchakick") or event.text.startswith("/captchakick") or event.text.startswith("?captchakick") or event.text.startswith("!captchakicktime") or event.text.startswith("/captchakicktime") or event.text.startswith("?captchakicktime") or event.text.startswith("!captchatime") or event.text.startswith("?captchatime") or event.text.startswith("/captchatime") or event.text.startswith("/captchamode") or event.text.startswith("?captchamode") or event.text.startswith("!captchamode"):
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
   await event.reply("That isn't a boolean - expected one of y/yes/on or n/no/off; got: {}".format(args))

@Cbot(pattern="^/captchakick ?(.*)")
async def _(event):
 if event.text.startswith("!captchakicktime") or event.text.startswith("?captchakicktime") or event.text.startswith("/captchakicktime"):
       return
 if event.is_private:
       return #connect
 if not await can_change_info(event, event.sender_id):
       return
 args = event.pattern_match.group(1)
 settings = sql.get_time(event.chat_id)
 if not args:
   if settings == False or settings == 0:
     await event.reply(ca_off)
   else:
     synctime = g_time(settings)
     await event.reply(ca_on.format(synctime))
 elif args in pos:
     if settings:
      synctime = g_time(settings)
     else:
      synctime = '5 Minutes'
      settings = 300
     await event.reply(f"I will now kick people that haven't solved the CAPTCHA after {synctime}.")
     sql.set_time(event.chat_id, settings)
 elif args in neg:
     await event.reply("I will no longer kick people that haven't solved the CAPTCHA.")
     sql.set_time(event.chat_id, 0)
 else:
     await event.reply("That isn't a boolean - expected one of y/yes/on or n/no/off; got: {args}")

@Cbot(pattern="^/captchakicktime ?(.*)")
async def _(event):
 if event.is_private:
       return #connect
 if not await can_change_info(event, event.sender_id):
       return
 args = event.pattern_match.group(1)
 settings = sql.get_time(event.chat_id)
 if not args:
   if settings == False or settings == 0:
     await event.reply(ca_ot)
   else:
     synctime = g_time(settings)
     await event.reply(ca_time.format(synctime))
 elif args:
     if len(args) == 1:
        return await event.reply(caut.format(args))
     time = await extract_time(event, args)
     if not time:
         return
     if time < 300 or time > 86400:
        return await event.reply("The welcome kick time can only be between 5 minutes, and 1 day. Please choose another time.")
     await event.reply(f"Welcome kick time has been set to {args}.")
     sql.set_time(event.chat_id, time)
     
@Cbot(pattern="^/captchatime ?(.*)")
async def _(event):
 if event.is_private:
       return #connect
 if not await can_change_info(event, event.sender_id):
       return
 args = event.pattern_match.group(1)
 settings = sql.get_unmute_time(event.chat_id)
 if not args:
  if settings == 0 or settings == False:
   await event.reply(smdd)
  else:
   value = g_time(settings)
   await event.reply(sudd.format(value))
 elif args:
     if len(args) == 1:
        return await event.reply(caut.format(args))
     time = await extract_time(event, args)
     if not time:
         return
     await event.reply(f"I will now mute people for {g_time(time)} when they join - or until they solve the CAPTCHA in the welcome message.")
     sql.set_unmute_time(event.chat_id, time)

@Cbot(pattern="^/captchamode ?(.*)")
async def _(event):
 if event.is_private:
       return #connect
 if not await can_change_info(event, event.sender_id):
       return
 args = event.pattern_match.group(1)
 settings = sql.get_style(event.chat_id)
 if not args:
   if settings == False or settings == 'button':
     await event.reply(bu_h)
   elif settings == 'text':
     await event.reply(tx_h)
   elif settings == 'math':
     await event.reply(mt_h)
 else:
  if not args in ['button', 'math', 'text']:
    await event.reply(f"'{args}' is not a recognised CAPTCHA mode! Try one of: button/math/text")
  else:
    text = f'CAPTCHA set to **{args}**\n'
    if args == 'button':
      text += "\nButton CAPTCHAs simply require a user to press a button in their welcome message to confirm they're human."
    elif args == 'math':
      text += "\nMath CAPTCHAs require the user to solve a basic maths question. Please note that this may discriminate against users with little maths knowledge."
    elif args == 'text':
      text += "\nText CAPTCHAs require the user to answer a CAPTCHA containing letters and numbers."
    await event.reply(text)
    sql.set_style(event.chat_id, args)

@tbot.on(events.ChatAction())
async def _(event):
 if not event.user_joined:
  return
 if sql.get_mode(event.chat_id) == False:
  return
 cws = cas.get_current_welcome_settings(event.chat_id)
 if not cws:
  string = f"Hey {event.user.first_name}, Welcome to {event.chat.title}! How are you?")
 else:
  user_id = event.user_id
  chattitle = event.chat.title
  first_name = event.user.first_name
  last_name = event.user.last_name
  username = event.user.username
  fullname = first_name
  if last_name:
   fullname = first_name + " " + last_name
  chat_id = event.chat_id
  mention = "[{first_name}](tg://user?id={user_id})"
  current_saved_welcome_message = None
  current_saved_welcome_message = cws.custom_welcome_message
  if "|" in current_saved_welcome_message:
   current_saved_welcome_message, button = current_saved_welcome_message.split("|")
   current_saved_welcome_message = current_saved_welcome_message.strip()
   button = button.strip()
   try:
    k = 0
    if "•" in button:
     mbutton = button.split("•")
     lbutton = [] 
     for i in mbutton:
      params = re.findall(r"\'(.*?)\'", i) or re.findall(r"\"(.*?)\"", i)
      lbutton.append(params)
      butto = []    
      if "[" or "]" in i:
       for c in lbutton:
         smd = [Button.url(*c)]
         butto.append(smd)
      else:
        for c in lbutton:
         smd = Button.url(*c)
         butto.append(smd)
    else:
     params = re.findall(r"\'(.*?)\'", button) or re.findall(r"\"(.*?)\"", button)
     butto = [Button.url(*params)]
   except:
     pass
  text = current_saved_welcome_message.format(
                                mention=mention,
                                chattitle=chattitle,
                                first=first_name,
                                last=last_name,
                                fullname=fullname,
                                userid=user_id,
                                username=username,
                            )

 await event.reply(text)

