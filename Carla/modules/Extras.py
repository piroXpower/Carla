from Carla.modules.sql.nightmode_sql import add_nightmode, rmnightmode, get_all_chat_id, is_nightmode_indb
from Carla import tbot
from Carla.events import Cbot
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
            await tbot.edit_permissions(event.chat_id, until_date=time.time() + (3600*6), send_messages=False)
        except Exception as e:
            logger.info(f"Unable To Close Group {chats.chat_id} - {e}")

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hour=11, minute=10)
scheduler.start()
