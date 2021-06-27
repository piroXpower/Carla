from Jessica.modules import db

welcome = db.welcome
goodbye = db.goodbye


def set_welcome(chat_id: int, w_text, id=None, hash=None, ref=None, type=None):
    welcome.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "text": w_text,
                "id": id,
                "hash": hash,
                "ref": ref,
                "mtype": type,
                "mode": True,
            }
        },
        upsert=True,
    )


def get_welcome(chat_id: int):
    _w = welcome.find_one({"chat_id": chat_id})
    if _w:
        return _w
    return None


def toggle_welcome(chat_id: int, mode):
    _w = welcome.find_one({"chat_id": chat_id})
    if _w:
        return welcome.update_one({"chat_id": chat_id}, {"$set": {"mode": mode}})
    welcome.insert_one(
        {
            "chat_id": chat_id,
            "text": None,
            "id": None,
            "hash": None,
            "ref": None,
            "mtype": None,
            "mode": mode,
        }
    )


def reset_welcome(chat_id: int):
    _w = welcome.find_one({"chat_id": chat_id})
    if _w:
        welcome.delete_one({"chat_id": chat_id})


def set_goodbye(chat_id: int, w_text, id=None, hash=None, ref=None, type=None):
    goodbye.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "text": w_text,
                "id": id,
                "hash": hash,
                "ref": ref,
                "mtype": type,
                "mode": True,
            }
        },
        upsert=True,
    )


def get_goodbye(chat_id: int):
    _w = goodbye.find_one({"chat_id": chat_id})
    if _w:
        return _w
    return None


def toggle_goodbye(chat_id: int, mode):
    _w = goodbye.find_one({"chat_id": chat_id})
    if _w:
        return goodbye.update_one({"chat_id": chat_id}, {"$set": {"mode": mode}})
    goodbye.insert_one(
        {
            "chat_id": chat_id,
            "text": None,
            "id": None,
            "hash": None,
            "ref": None,
            "mtype": None,
            "mode": mode,
        }
    )


def reset_goodbye(chat_id: int):
    _w = goodbye.find_one({"chat_id": chat_id})
    if _w:
        goodbye.delete_one({"chat_id": chat_id})
