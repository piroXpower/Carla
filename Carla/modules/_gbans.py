from Carla import tbot, OWNER_ID
from . import ELITES, SUDO_USERS, is_admin
from Carla.events import Cbot

a = """
__Your request sent to DEVS waiting for approval. Till that send proofs to DEVS.__
"""

@Cbot(pattern="^/gban ?(.*)")
async def _(event):
 await event.reply(a)
