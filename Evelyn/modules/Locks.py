# soon


async def delete_locked(event, locks=[]):
    if "sticker" in locks:
        if event.sticker:
            if event.chat.admin_rights.delete_messages:
                await event.delete()
    elif "gif" in locks:
        if event.gif:
            if event.chat.admin_rights.delete_messages:
                await event.delete()
    elif "phone" in locks:
        print("soon")
    elif "audio" in locks:
        if event.audio:
            if event.chat.admin_rights.delete_messages:
                await event.delete()
    elif "video" in locks:
        if event.video:
            if event.chat.admin_rights.delete_messages:
                await event.delete()
    elif "album" in locks:
        if event.album:
            if event.chat.admin_rights.delete_messages:
                await event.delete()
    elif "emoji" in locks:
        print("soon")
    elif "emojigame" in locks:
        print("soon")
