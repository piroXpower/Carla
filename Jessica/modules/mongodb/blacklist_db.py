from .. import db

blacklist = db.blacklist


def add_to_blacklist(chat_id, trigger):
    _bl = blacklist.find_one({"chat_id": chat_id})
    if _bl:
        bl = _bl["blacklists"]
        mode = _bl["mode"]
        time = _bl["time"]
    else:
        bl = []
        mode = "nothing"
        time = 0
    bl.append(trigger)
    blacklist.update_one(
        {"chat_id": chat_id},
        {"$set": {"blacklists": bl, "mode": mode, "time": time}},
        upsert=True,
    )


def rm_from_blacklist(chat_id, trigger):
    _bl = blacklist.find_one({"chat_id": chat_id})
    if _bl:
        bl = _bl["blacklists"]
    else:
        return False
    if trigger in bl:
        bl.remove(trigger)
    blacklist.update_one(
        {"chat_id": chat_id}, {"$set": {"blacklists": bl}}, upsert=True
    )
