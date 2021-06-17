from sqlalchemy import Column, Integer, UnicodeText

from . import BASE, SESSION


class SUDO(BASE):
    __tablename__ = "sudousers"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(UnicodeText)

    def __init__(self, user_id, first_name):
        self.user_id = user_id
        self.first_name = first_name


class ELITE(BASE):
    __tablename__ = "eliteusers"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(UnicodeText)

    def __init__(self, user_id, first_name):
        self.user_id = user_id
        self.first_name = first_name


SUDO.__table__.create(checkfirst=True)
ELITE.__table__.create(checkfirst=True)


def add_sudo(user_id, first_name):
    sudo = SESSION.query(SUDO).get(str(user_id))
    if sudo:
        return False
    sudo = SUDO(user_id, first_name)
    SESSION.add(sudo)
    SESSION.commit()
    return True


def remove_sudo(user_id):
    sudo = SESSION.query(SUDO).get(str(user_id))
    if sudo:
        SESSION.delete(sudo)
        SESSION.commit()
        return True
    return False


def get_all_sudos():
    try:
        return SESSION.query(SUDO).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_elite(user_id, first_name):
    el = SESSION.query(ELITE).get(str(user_id))
    if el:
        return False
    el = ELITE(user_id, first_name)
    SESSION.add(el)
    SESSION.commit()
    return True


def remove_elite(user_id):
    sudo = SESSION.query(ELITE).get(str(user_id))
    if sudo:
        SESSION.delete(sudo)
        SESSION.commit()
        return True
    return False


def get_all_elites():
    try:
        return SESSION.query(ELITE).all()
    except BaseException:
        return None
    finally:
        SESSION.close()
