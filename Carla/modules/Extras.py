from Carla.modules.sql.nightmode_sql import add_nightmode, rmnightmode, get_all_chat_id, is_nightmode_indb
from Carla import tbot
from Carla.events import Cbot
import time, wget, json
from requests import get
from . import can_change_info
from apscheduler.schedulers.asyncio import AsyncIOScheduler

enable = ['enable', 'on', 'y', 'yes']
disable = ['disable', 'off', 'n' 'no']

@Cbot(pattern="^/nightmode ?(.*)")
async def lilz(event):
 if event.is_private:
    return
 if not await can_change_info(event, event.sender_id):
    return
 args = event.pattern_match.group(1)
 if not args:
   if is_nightmode_indb(event.chat_id):
      await event.reply("**NightMode** is currently **enabled** for this chat.")
   else:
      await event.reply("**NightMode** is currently **disabled** for this chat.")
 elif args in enable:
      await event.reply("Enabled nightmode for this.\n\nGroup closes at 12Am and opens at 6Am IST")
      add_nightmode(event.chat_id)
 elif args in disable:
      await event.reply("Disabled nightmode for this chat.")
      rmnightmode(event.chat_id)

async def job_close():
    nt_chats = get_all_chat_id()
    if len(nt_chats) == 0:
        return
    for chats in nt_chats:
        try:
            await tbot.send_message(
              int(chats.chat_id), "12:00 Am, Group Is Closing Till 6 Am. Night Mode Started ! \n**Powered By CarLa**"
            )
            await tbot.edit_permissions(int(chats.chat_id), send_messages=False)
        except Exception as e:
            logger.info(f"Unable To Close Group {chats.chat_id} - {e}")

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hour=23, minute=58)
scheduler.start()

async def job_open():
    nt_chats = get_all_chat_id()
    if len(nt_chats) == 0:
        return
    for chats in nt_chats:
        try:
            await tbot.send_message(
              int(chats.chat_id), "06:00 Am, Group Is Opening.\n**Powered By CarLa**"
            )
            await tbot.edit_permissions(int(chats.chat_id), send_messages=True)
        except Exception as e:
            logger.info(f"Unable To Open Group {chats.chat_id} - {e}")

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_open, trigger="cron", hour=6, minute=1)
scheduler.start()


@Cbot(pattern="^/(GitHub|github) ?(.*)")
async def gt(event):
 arg = event.pattern_match.group(2)
 git = get(f"https://api.github.com/users/{arg}").json()
 try:
  if git["type"] == 'User':
    text = "<b>User Info:</b>"
  else:
    text = "<b>Organization Info:</b>"
 except KeyError:
  pass
 try:
  name = git["name"]
  text += f"\n<b>Name:</b> {name}"
 except KeyError:
  pass
 try:
  id = git["id"]
  text += f"\n<b>ID:</b> <code>{id}</code>"
 except KeyError:
  pass
 try:
  nid = git["node_id"]
  text += f"\n<b>Node ID:</b> {nid}"
 except KeyError:
  pass
 try:
  company = git["company"]
  if not company == None:
   text += f"\n<b>Company:</b> {company}"
 except KeyError:
  pass
 try:
  followers = git["followers"]
  if not followers == None:
   text += f"\n<b>Followers:</b> {followers}"
 except KeyError:
  pass
 try:
  blog = git["blog"]
  if not blog == None:
   text += f"\n<b>Blog:</b> <code>{blog}</code>"
 except KeyError:
  pass
 try:
  location = git["location"]
  if not location == None:
   text += f"\n<b>Location:</b> {location}"
 except KeyError:
  pass
 try:
  bio = git["bio"]
  if not bio == None:
   text += f"\n\n<b>Bio:</b> <code>{bio}</code>"
 except KeyError:
  pass
 try:
  twitter = git["twitter_username"]
  if not twitter == None:
   text += f"\n\n<b>Twitter:</b> {twitter}"
 except KeyError:
  pass
 try:
  email = git["email"]
  if not email == None:
   text += f"\n<b>Email:</b> <code>{email}</code>"
 except KeyError:
  pass
 try:
  repo = git["public_repos"]
  text += f"\n<b>Repos:</b> {repo}"
 except KeyError:
  pass
 try:
  url = git["html_url"]
  text += f"\n\n<b>URL:</b> <code>{url}</code>"
 except KeyError:
  pass
 await event.respond(text, parse_mode='html')
 
@Cbot(pattern="^/repo ?(.*)")
async def lo(event):
 arg = event.pattern_match.group(1)
 usr = get(f"https://api.github.com/users/{arg}/repos?per_page=40").json()
 reply_text = "<b>Repo:</b>"
 for i in range(len(usr)):
   reply_text += f'\n<a href="{usr[i]["html_url"]}">{usr[i]["name"]}</a>'
 await event.respond(reply_text, parse_mode='htm', link_preview=False)

@tbot.on(events.InlineQuery(pattern="imdb ?(.*)")
async def im(event):
 query = event.pattern_match.group(1)
 builder = event.builder
 
