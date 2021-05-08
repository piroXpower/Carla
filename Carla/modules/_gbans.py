from Carla import tbot, OWNER_ID
from . import ELITES, SUDO_USERS, is_admin, get_user
from Carla.events import Cbot

a = """
__Your request sent to DEVS waiting for approval. Till that send proofs to DEVS.__
"""
b = """
You don't seem to be referring to a user or the ID specified is incorrect..
"""

@Cbot(pattern="^/gban ?(.*)")
async def _(event):
 if not event.sender_id == OWNER_ID or event.sender_id in ELITES or event.sender_id in SUDO_USERS:
   return
 if not event.reply_to_msg_id and not event.pattern_match.group(1):
   return await event.reply(b)
 user, extra = await get_user(event)
 await event.respond(f'{user.first_name} {extra}')
