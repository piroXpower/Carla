from sqlalchemy import Boolean, Column, String, UnicodeText

from . import BASE, SESSION


class NOTES(BASE):
    __tablename__ = "notes"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True)
    reply = Column(UnicodeText)
    file = Column(UnicodeText, default=None)

    def __init__(
        self,
        chat_id,
        keyword,
        reply,
        file,
    ):
        self.chat_id = chat_id
        self.keyword = keyword
        self.reply = reply
        self.file = file


class PRIV(BASE):
    __tablename__ = "privnotes"
    chat_id = Column(String(14), primary_key=True)
    mode = Column(Boolean, default=False)

    def __init__(self, chat_id, mode=False):
        self.chat_id = chat_id
        self.mode = mode


NOTES.__table__.create(checkfirst=True)
PRIV.__table__.create(checkfirst=True)


def set_mode(chat_id, mode):
    adder = SESSION.query(PRIV).get(str(chat_id))
    if adder:
        adder.mode = mode
    else:
        adder = PRIV(chat_id, mode)
    SESSION.add(adder)
    SESSION.commit()


def get_mode(chat_id):
    try:
        k = SESSION.query(PRIV).get(str(chat_id))
        return k.mode
    except BaseException:
        return False
    finally:
        SESSION.close()


def get_notes(chat_id, keyword):
    try:
        return SESSION.query(NOTES).get((str(chat_id), keyword))
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_all_notes(chat_id):
    try:
        return SESSION.query(NOTES).filter(NOTES.chat_id == str(chat_id)).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_note(chat_id, keyword, reply, file=None):
    adder = SESSION.query(NOTES).get((str(chat_id), keyword))
    if adder:
        adder.reply = reply
        adder.file = file
    else:
        adder = NOTES(chat_id, keyword, reply, file)
        adder = NOTES(
            chat_id,
            keyword,
            reply,
            file,
        )
    SESSION.add(adder)
    SESSION.commit()


def remove_note(chat_id, keyword):
    saved_note = SESSION.query(NOTES).get((str(chat_id), keyword))
    if saved_note:
        SESSION.delete(saved_note)
        SESSION.commit()


def remove_all_notes(chat_id):
    saved_note = SESSION.query(NOTES).filter(NOTES.chat_id == str(chat_id))
    if saved_note:
        saved_note.delete()
        SESSION.commit()
