# from . import db
# from ..events import Cbot, Cinline
from .. import tbot, CMD_HELP
from telethon.tl.types import ChannelParticipantBanned, UpdateChannelParticipant

@tbot.events.Raw(UpdateChannelParticipant)
async def x(e):
 if not e.prev_participant:
        return
 if isinstance(e.prev_participant, ChannelParticipantBanned):
        return
 if e.channel_id == 1486931338:
   pass
 else:
   return
 chat_id = int((-100) + str(e.channel_id ))
 await tbot.send_message(chat_id, "AntiBetreyal_Sys Test.")
