from Carla import tbot
from Carla.events import Cbot
from . import can_ban_users


async def excecute_operation(event, user_id, name, mode, reason="", tt=""):
           if mode == 'ban':
                 await tbot.edit_permissions(event.chat_id, user_id, until_date=None, view_messages=False)
                 if reason:
                     reason = f"\nReason: <code>{reason}</code>"
                 await event.respond(f'<b>Banned <a href="tg://user?id={user_id}">{name}</a></b>!{reason}', parse_mode='html')
           elif mode == 'kick':
                 await tbot.kick_participant(event.chat_id, event.sender_id)
                 if reason:
                     reason = f"\nReason: <code>{reason}</code>"
                 await event.respond(f'<b>Kicked <a href="tg://user?id={user_id}">{name}</a></b>!{reason}', parse_mode='html')
           elif mode == 'mute':
                 await tbot.edit_permissions(event.chat_id, event.sender_id, until_date=None, send_messages=False)
                 if reason:
                     reason = f"\nReason: <code>{reason}</code>"
                 await event.respond(f'<b>Muted <a href="tg://user?id={user_id}">{name}</a></b>!{reason}', parse_mode='html')
           elif mode == 'tban':
                 tt = sql.get_time(event.chat_id)
                 await tbot.edit_permissions(event.chat_id, event.sender_id, until_date=time.time() + int(tt), view_messages=False)
           elif mode == 'tmute':
                 if reason:
                     reason = f"\nReason: <code>{reason}</code>"
                 await event.respond(f'<b>Muted <a href="tg://user?id={user_id}">{name}</a></b> for !{reason}', parse_mode='html')
                 await tbot.edit_permissions(event.chat_id, event.sender_id, until_date=time.time() + int(tt), send_messages=False)
