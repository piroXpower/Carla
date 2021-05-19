from sqlalchemy import Boolean, Column, String

from . import BASE, SESSION


class AD(BASE):
    __tablename__ = "anti_advetisements"
    chat_id = Column(String(14), primary_key=True)
    mode = Column(Boolean, default=False)

    def __init__(self, chat_id, mode=False):
        self.chat_id = chat_id
        self.mode = mode


AD.__table__.create(checkfirst=True)


def add_ad(chat_id: str, mode):
    ad = SESSION.query(AD).get(str(chat_id))
    if ad:
        ad.mode = mode
    else:
        ad = AD(str(chat_id), mode)
    SESSION.add(ad)
    SESSION.commit()


def ad_settings(chat_id: str):
    try:
        s__ = SESSION.query(AD).get(str(chat_id))
        if s__:
            return s__.mode
        return False
    finally:
        SESSION.close()
