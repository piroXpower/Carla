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


def update_clean_welcome(chat_id, mode):
    row = SESSION.query(Welcome).get(str(chat_id))
    row.should_clean_welcome = mode
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
    __tablename__ = "wlc_settings"
    chat_id = Column(String(14), primary_key=True)
    mode = Column(Boolean, default=True)
    clean_service = Column(Boolean, default=False)

    def __init__(self, chat_id, mode=True, clean_service=False):
        self.chat_id = chat_id
        self.mode = mode
        self.clean_service = clean_service


class GB(BASE):
    __tablename__ = "gooudbye"
    chat_id = Column(String(14), primary_key=True)
    mode = Column(Boolean, default=True)

    def __init__(self, chat_id, mode=True):
        self.chat_id = chat_id
        self.mode = mode


Wlc.__table__.create(checkfirst=True)
GB.__table__.create(checkfirst=True)


def set_welcome_mode(chat_id: str, mode):
    wel = SESSION.query(Wlc).get(str(chat_id))
    if wel:
        wel.mode = mode
    else:
        wel = Wlc(chat_id, mode, False)
    SESSION.add(wel)
    SESSION.commit()


def welcome_mode(chat_id: str):
    wel = SESSION.query(Wlc).get(str(chat_id))
    if wel:
        return wel.mode
    return True


def set_clean_service(chat_id: str, mode):
    wel = SESSION.query(Wlc).get(str(chat_id))
    if wel:
        wel.clean_service = mode
    else:
        wel = Wlc(chat_id, True, mode)
    SESSION.add(wel)
    SESSION.commit()


def get_clean_service(chat_id):
    wel = SESSION.query(Wlc).get(str(chat_id))
    if wel:
        return wel.clean_service
    return False


def set_goodbye_mode(chat_id: str, mode):
    goodb = SESSION.query(GB).get(str(chat_id))
    if goodb:
        goodb.mode = mode
    else:
        goodb = GB(chat_id, mode)
    SESSION.add(goodb)
    SESSION.commit()


def goodbye_mode(chat_id: str):
    goodb = SESSION.query(GB).get(str(chat_id))
    if goodb:
        return goodb.mode
    return True
