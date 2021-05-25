from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

from Evelyn import tbot


def participant_check(channel, user_id):
    try:
        result = await tbot(GetParticipantRequest(channel=channel, user_id=user_id))
        return True
    except UserNotParticipantError:
        return False
