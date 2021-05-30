from sqlalchemy import BigInteger, Boolean, Column, String, UnicodeText

from . import BASE, SESSION


class Welcome(BASE):
    __tablename__ = "welcome"
    chat_id = Column(String(14), primary_key=True)
    custom_welcome_message = Column(UnicodeText)
    media_file_id = Column(UnicodeText)
    should_clean_welcome = Column(Boolean, default=False)
    previous_welcome = Column(BigInteger)

    def __init__(
        self,
        chat_id,
        custom_welcome_message,
        should_clean_welcome,
        previous_welcome,
        media_file_id=None,
    ):
        self.chat_id = chat_id
        self.custom_welcome_message = custom_welcome_message
        self.media_file_id = media_file_id
        self.should_clean_welcome = should_clean_welcome
        self.previous_welcome = previous_welcome


class Goodbye(BASE):
    __tablename__ = "goodbye"
    chat_id = Column(String(14), primary_key=True)
    custom_goodbye_message = Column(UnicodeText)
    media_file_id = Column(UnicodeText)
    should_clean_goodbye = Column(Boolean, default=False)
    previous_goodbye = Column(BigInteger)

    def __init__(
        self,
        chat_id,
        custom_goodbye_message,
        should_clean_goodbye,
        previous_goodbye,
        media_file_id=None,
    ):
        self.chat_id = chat_id
        self.custom_goodbye_message = custom_goodbye_message
        self.media_file_id = media_file_id
        self.should_clean_goodbye = should_clean_goodbye
        self.previous_goodbye = previous_goodbye


Welcome.__table__.create(checkfirst=True)
Goodbye.__table__.create(checkfirst=True)


def get_current_welcome_settings(chat_id):
    try:
        return SESSION.query(Welcome).filter(Welcome.chat_id == str(chat_id)).one()
    except:
        return None
    finally:
        SESSION.close()


def add_welcome_setting(
    chat_id,
    custom_welcome_message,
    should_clean_welcome,
    previous_welcome,
    media_file_id,
):
    # adder = SESSION.query(Welcome).get(chat_id)
    adder = Welcome(
        chat_id,
        custom_welcome_message,
        should_clean_welcome,
        previous_welcome,
        media_file_id,
    )
    SESSION.add(adder)
    SESSION.commit()


def rm_welcome_setting(chat_id):
    rem = SESSION.query(Welcome).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def update_previous_welcome(chat_id, previous_welcome):
    row = SESSION.query(Welcome).get(str(chat_id))
    row.previous_welcome = previous_welcome
    # commit the changes to the DB
    SESSION.commit()


def get_current_goodbye_settings(chat_id):
    try:
        return SESSION.query(Goodbye).filter(Goodbye.chat_id == str(chat_id)).one()
    except:
        return None
    finally:
        SESSION.close()


def add_goodbye_setting(
    chat_id,
    custom_goodbye_message,
    should_clean_goodbye,
    previous_goodbye,
    media_file_id,
):
    # adder = SESSION.query(Goodbye).get(chat_id)
    adder = Goodbye(
        chat_id,
        custom_goodbye_message,
        should_clean_goodbye,
        previous_goodbye,
        media_file_id,
    )
    SESSION.add(adder)
    SESSION.commit()


def rm_goodbye_setting(chat_id):
    rem = SESSION.query(Goodbye).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def update_previous_goodbye(chat_id, previous_goodbye):
    row = SESSION.query(Goodbye).get(str(chat_id))
    row.previous_goodbye = previous_goodbye
    # commit the changes to the DB
    SESSION.commit()


class Wlc(BASE):
    __tablename__ = "sumd"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


class GB(BASE):
    __tablename__ = "gudbye"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Wlc.__table__.create(checkfirst=True)
GB.__table__.create(checkfirst=True)


def add_c(chat_id: str):
    rmnightmoddy = SESSION.query(Wlc).get(str(chat_id))
    if rmnightmoddy:
        return
    nightmoddy = Wlc(str(chat_id))
    SESSION.add(nightmoddy)
    SESSION.commit()


def add_gb(chat_id: str):
    rmnightmoddy = SESSION.query(GB).get(str(chat_id))
    if rmnightmoddy:
        return
    nightmoddy = GB(str(chat_id))
    SESSION.add(nightmoddy)
    SESSION.commit()


def rm_gb(chat_id: str):
    rmnightmoddy = SESSION.query(GB).get(str(chat_id))
    if rmnightmoddy:
        SESSION.delete(rmnightmoddy)
        SESSION.commit()


def rmc(chat_id: str):
    rmnightmoddy = SESSION.query(Wlc).get(str(chat_id))
    if rmnightmoddy:
        SESSION.delete(rmnightmoddy)
        SESSION.commit()


def is_chat(chat_id: str):
    try:
        s__ = SESSION.query(Wlc).get(str(chat_id))
        if s__:
            return False
        return True
    finally:
        SESSION.close()


def is_gb(chat_id: str):
    try:
        s__ = SESSION.query(GB).get(str(chat_id))
        if s__:
            return False
        return True
    finally:
        SESSION.close()
