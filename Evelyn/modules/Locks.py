# soon


async def delete_locked(event, locks=[]):
    if not event.chat.admin_rights.delete_messages:
        return
    if "sticker" in locks:
        if event.sticker:
            await event.delete()
    elif "gif" in locks:
        if event.gif:
            await event.delete()
    elif "phone" in locks:
        print("soon")
    elif "audio" in locks:
        if event.audio:
            await event.delete()
    elif "video" in locks:
        if event.video:
            await event.delete()
    elif "emoji" in locks:
        print("soon")
    if "inline" in locks:
       if event.via_bot_id:
         await event.delete()
    elif "emojigame" in locks:
        if event.media:
            if event.media.emoticon:
                if event.media.emoticon in ["🎰", "⚽", "🏀", "🎯", "🎲"]:
                    await event.delete()

