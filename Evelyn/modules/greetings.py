import Evelyn.modules.mongodb.welcome_db as db
from . import can_change_info

@Cbot(pattern="^/setwelcome ?(.*)")
async def set_welxome(event):
 
