from Evelyn import tbot
from Evelyn.events import Cbot
from . import is_admin, can_ban_users, is_owner
from telethon import events, Button
import Evelyn.modules.sql.fsub_sql as sql
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError

def participant_check(channel, user_id):
 try:
   result = await tbot(GetParticipantRequest(channel=channel, user_id=user_id))
   return True
 except UserNotParticipantError:
   return False
