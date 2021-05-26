from sqlalchemy import Column, String, UnicodeText

from . import BASE, SESSION


class FILTERS(BASE):
    __tablename__ = "filters"
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


FILTERS.__table__.create(checkfirst=True)


def get_filters(chat_id, keyword):
    try:
        return SESSION.query(FILTERS).get((str(chat_id), keyword))
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_all_filters(chat_id):
    try:
        return SESSION.query(FILTERS).filter(FILTERS.chat_id == str(chat_id)).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_filter(chat_id, keyword, reply, file=None):
    adder = SESSION.query(FILTERS).get((str(chat_id), keyword))
    if adder:
        adder.reply = reply
        adder.file = file
    else:
        adder = FILTERS(chat_id, keyword, reply, file)
        adder = FILTERS(
            chat_id,
            keyword,
            reply,
            file,
        )
    SESSION.add(adder)
    SESSION.commit()


def remove_filter(chat_id, keyword):
    saved_note = SESSION.query(FILTERS).get((str(chat_id), keyword))
    if saved_note:
        SESSION.delete(saved_note)
        SESSION.commit()


def remove_all_filters(chat_id):
    saved_note = SESSION.query(FILTERS).filter(FILTERS.chat_id == str(chat_id))
    if saved_note:
        saved_note.delete()
        SESSION.commit()
