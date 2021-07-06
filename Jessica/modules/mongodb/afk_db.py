import time

from .. import db

afk = db.afk


def set_afk(user_id: int, first_name="User", reason=None):
    afk.insert_one(
        {
            "user_id": user_id,
            "first_name": first_name,
            "reason": reason,
            "time": time.time(),
        }
    )


def unset_afk(user_id):
    _afk = afk.find_one({"user_id": user_id})
    if _afk:
        afk.delete_one({"user_id": user_id})


def is_afk(user_id):
    _afk = afk.find_one({"user_id": user_id})
    if _afk:
        return True
    return False

def get_afk(user_id):
 _afk = afk.find_one({"user_id": user_id})
 if _afk:
        return _afk
 return False
