import threading

from sqlalchemy import Boolean, Column, String, UnicodeText, distinct, func

from . import BASE, SESSION


class Rules(BASE):
    __tablename__ = "rules"
    chat_id = Column(String(14), primary_key=True)
    rules = Column(UnicodeText, default="")

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def __repr__(self):
        return "<Chat {} rules: {}>".format(self.chat_id, self.rules)


class Prules(BASE):
    __tablename__ = "privaterules"
    chat_id = Column(String(14), primary_key=True)
    mode = Column(Boolean, default=False)
    button = Column(UnicodeText, default="Rules")

    def __init__(self, chat_id, mode=False, button="Rules"):
        self.chat_id = chat_id
        self.mode = mode
        self.button = button


Rules.__table__.create(checkfirst=True)
Prules.__table__.create(checkfirst=True)


INSERTION_LOCK = threading.RLock()


def set_rules(chat_id, rules_text):
    with INSERTION_LOCK:
        rules = SESSION.query(Rules).get(str(chat_id))
        if not rules:
            rules = Rules(str(chat_id))
        rules.rules = rules_text

        SESSION.add(rules)
        SESSION.commit()


def get_rules(chat_id):
    rules = SESSION.query(Rules).get(str(chat_id))
    ret = ""
    if rules:
        ret = rules.rules

    SESSION.close()
    return ret


def num_chats():
    try:
        return SESSION.query(func.count(distinct(Rules.chat_id))).scalar()
    finally:
        SESSION.close()


def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        chat = SESSION.query(Rules).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)
        SESSION.commit()


def set_private_rules(chat_id, mode):
    with INSERTION_LOCK:
        rules_m = SESSION.query(Prules).get(str(chat_id))
        if not rules_m:
            rules_m = Prules(str(chat_id), mode, "Rules")
        rules_m.mode = mode

        SESSION.add(rules_m)
        SESSION.commit()


def set_button(chat_id: int, btn: str):
    with INSERTION_LOCK:
        rules_m = SESSION.query(Prules).get(str(chat_id))
        if not rules_m:
            rules_m = Prules(str(chat_id), False, btn)
        rules_m.button = btn

        SESSION.add(rules_m)
        SESSION.commit()


def get_private(chat_id):
    try:
        return (SESSION.query(Prules).get(str(chat_id))).mode
    except BaseException:
        return False
    finally:
        SESSION.close()


def get_button(chat_id):
    try:
        return (SESSION.query(Prules).get(str(chat_id))).button
    except BaseException:
        return "Rules"
    finally:
        SESSION.close()
