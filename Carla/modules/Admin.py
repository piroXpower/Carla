from Carla import tbot, OWNER_ID
from Carla.events import Cbot
from . import ELITES, can_promote_users

@Cbot(pattern="^/promote ?(.*)")
async def _(event):
 

