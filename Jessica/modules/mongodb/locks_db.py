from Jessica.modules import db

locks = db.locks


def add_lock(chat_id, type):
    _locks = locks.find_one({"chat_id": chat_id})
    if _locks:
        _lock = _locks["locked"]
    else:
        _lock = []
    _lock.append(type)
    new_lock = list(set(_lock))
    locks.update_one({"chat_id": chat_id}, {"$set": {"locked": new_lock}}, upsert=True)


def get_locks(chat_id):
    _locks = locks.find_one({"chat_id": chat_id})
    if _locks:
        return _locks["locked"]
    return None

def remove_lock(chat_id, type):
 _locks = locks.find_one({"chat_id": chat_id})
 if _locks:
        _lock = _locks["locked"]
 else:
        return
 if type in _lock:
   _lock.remove(type)
   locks.update_one({"chat_id": chat_id}, {"$set": {"locked": _lock}}, upsert=True)

all_locks = [media,
            audio,
            video,
            sticker,
            gif,
            inline,
            all,
            emojigame,
            phone,
            photo,
            url,
            location,
            invitelink,
            forward,
            document,
            contact,
            command,
            button,
            bot,
            email,
            game,
            text,
            voice,
            videonote,
            poll,
        ]

def lock_all(chat_id):
 locks.update_one({"chat_id": chat_id}, {"$set": {"locked": all_locks}}, upsert=True)
