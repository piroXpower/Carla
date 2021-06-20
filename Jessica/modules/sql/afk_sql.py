import threading
from . import BASE, SESSION
from sqlalchemy import Boolean, Column, Integer, UnicodeText, String


class AFK(BASE):
    __tablename__ = "afk_users"

    user_id = Column(Integer, primary_key=True)
    is_afk = Column(Boolean)
    reason = Column(UnicodeText)
    fname = Column(UnicodeText)

    def __init__(self, user_id, reason="", is_afk=True, fname=""):
        self.user_id = user_id
        self.reason = reason
        self.is_afk = is_afk
        self.fname = fname

    def __repr__(self):
        return "afk_status for {}".format(self.user_id)


AFK.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

AFK_USERS = {}
AFK_USERSS = {}

def is_afk(user_id):
    return user_id in AFK_USERS
    return user_id in AFK_USERSS


def check_afk_status(user_id):
    try:
        return SESSION.query(AFK).get(user_id)
    finally:
        SESSION.close()


def set_afk(user_id, reason, fname=""):
    with INSERTION_LOCK:
        curr = SESSION.query(AFK).get(user_id)
        if not curr:
            curr = AFK(user_id, reason, True, fname)
        else:
            curr.is_afk = True
            curr.reason = reason
            curr.fname = fname
        AFK_USERS[user_id] = reason
        AFK_USERSS[user_id] = fname
        SESSION.add(curr)
        SESSION.commit()


def rm_afk(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(AFK).get(user_id)
        if curr:
            if user_id in AFK_USERS:  # sanity check
                del AFK_USERS[user_id]
                del AFK_USERSS[user_id]
            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def __load_afk_users():
    global AFK_USERS
    global AFK_USERSS
    try:
        all_afk = SESSION.query(AFK).all()
        AFK_USERS = {user.user_id: user.reason for user in all_afk if user.is_afk}
        AFK_USERSS = {user.user_id: user.fname for user in all_afk if user.is_afk}
    finally:
        SESSION.close()


__load_afk_users()
