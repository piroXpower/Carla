from .. import db

antiflood = db.antiflood

CHAT_FLOOD = {}


def set_flood(chat_id, amount=3):
    _flood = antiflood.find_one({"chat_id": chat_id})
    if _flood:
        mode = _flood["mode"]
        time = _flood["time"]
    else:
        mode = "ban"
        time = 0
    antiflood.update_one(
        {"chat_id": chat_id},
        {"$set": {"value": amount, "mode": mode, "time": time}},
        upsert=True,
    )


def update_flood(chat_id, user_id):
    if not CHAT_FLOOD.get("chat_id"):
        old_id = None
        c = 0
    else:
        c = CHAT_FLOOD[chat_id][1]
        old_id = CHAT_FLOOD[chat_id][0]
    if user_id != old_id:
        CHAT_FLOOD[chat_id] = (user_id, 1)
        return False
    else:
        d = antiflood.find_one({"chat_id": chat_id})
        if d:
            limit = d.get("value")
        else:
            limit = 3
        c += 1
        if c >= limit:
            CHAT_FLOOD[chat_id] = (user_id, 0)
            return True
        CHAT_FLOOD[chat_id] = (user_id, c)
        return False
