from .. import db

warns = db.warns


def warn_user(user_id, chat_id, reason=""):
    _warn = warns.find_one({"chat_id": chat_id, "user_id": user_id})
    if _warn:
        reasons = (_warn["reasons"]).append(reason)
        num_warns = _warn["num_warns"] + 1
    else:
        reasons = [reason]
        num_warns = 1
    warns.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"reasons": reasons, "num_warns": num_warns}},
        upsert=True,
    )


def remove_warn(user_id, chat_id):
    _warn = warns.find_one({"chat_id": chat_id, "user_id": user_id})
    if _warn and _warn["num_warns"] > 0:
        warns.update_one(
            {"chat_id": chat_id, "user_id": user_id},
            {"$set": {"num_warns": _warn["num_warns"] - 1}},
            upsert=True,
        )
        return True
    return False


def reset_warns(user_id, chat_id):
    _warn = warns.find_one({"chat_id": chat_id, "user_id": user_id})
    if _warn:
        warns.update_one(
            {"chat_id": chat_id, "user_id": user_id},
            {"$set": {"num_warns": 0}},
            upsert=True,
        )
        return True
    return False


def get_warns(user_id, chat_id):
    _warn = warns.find_one({"chat_id": chat_id, "user_id": user_id})
    if _warn:
        return _warn["num_warns"], _warn["reasons"]
    return None


def reset_all_warns(chat_id):
    warns.delete_one({"chat_id": chat_id})


# soon
