from Carla import tbot, OWNER_ID
from . import ELITES, SUDO_USERS, is_admin
from Carla.events import Cbot

a = """
__Your request sent to DEVS waiting for approval. Till that send proofs to DEVS.__
"""
b = """
You don't seem to be referring to a user or the ID specified is incorrect..
"""

@Cbot(pattern="^/gban ?(.*)")
async def _(event):
 if not event.reply_to_msg_id and not event.pattern_match.group(1):
   return await event.reply(b)
