import Jessica.modules.mongodb.locks_db as db
from Jessica.events import Cbot

from . import can_change_info


@Cbot(pattern="^/lock ?(.*)")
async def lock_item(event):
    if event.is_private:
        return await event.reply("This command is made to be used in group chats.")
    if event.is_group and event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    if not event.pattern_match.group(1):
        return await event.reply("You haven't specified a type to lock.")
    lock_items = event.text.split(None, 1)[1]
    locks = lock_items.split(None)
    lock_s = []
    av_locks = db.all_locks
    for lock in locks:
        if lock in av_locks:
            lock_s.append(lock)
    if "all" in locks:
        db.lock_all(event.chat_id)
        await event.reply("Locked `all`")
        try:
            await tbot.edit_permissions(event.chat_id, send_messages=False)
        except:
            pass
        return
    if len(lock_s) == 0:
        await event.reply(f"Unknown lock types:- {lock_items}\nCheck /locktypes!")
    else:
        text = "Locked"
        for i in lock_s:
            text = text + f" `{i}`"
        await event.reply(text)
    for lock in lock_s:
        db.add_lock(event.chat_id, lock)
    if "text" in lock_s:
        try:
            await tbot.edit_permissions(event.chat_id, send_messages=False)
        except:
            pass
    if "media" in lock_s:
        try:
            await tbot.edit_permissions(event.chat_id, send_media=False)
        except:
            pass
    if "inline" in lock_s:
        try:
            await tbot.edit_permissions(event.chat_id, send_inline=False)
        except:
            pass
