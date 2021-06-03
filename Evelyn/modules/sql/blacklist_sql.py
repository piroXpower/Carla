import threading

from sqlalchemy import Column, Integer, String, UnicodeText, distinct, func

from . import BASE, SESSION


class BlackListFilters(BASE):
    __tablename__ = "sl"
    chat_id = Column(String(14), primary_key=True)
    trigger = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, chat_id, trigger):
        self.chat_id = str(chat_id)  # ensure string
        self.trigger = trigger

    def __repr__(self):
        return "<Blacklist filter '%s' for %s>" % (self.trigger, self.chat_id)

    def __eq__(self, other):
        return bool(
            isinstance(other, BlackListFilters)
            and self.chat_id == other.chat_id
            and self.trigger == other.trigger
        )


class BlSticker(BASE):
    __tablename__ = "slst"
    chat_id = Column(String(14), primary_key=True)
    sticker = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, chat_id, sticker):
        self.chat_id = str(chat_id)  # ensure string
        self.sticker = sticker

    def __repr__(self):
        return "<Blacklist sticker '%s' for %s>" % (self.sticker, self.chat_id)

    def __eq__(self, other):
        return bool(
            isinstance(other, BlSticker)
            and self.chat_id == other.chat_id
            and self.sticker == other.sticker
        )


class BlackListMode(BASE):
    __tablename__ = "blackmoda"
    chat_id = Column(String(14), primary_key=True)
    mode = Column(UnicodeText, default="nothing")
    time = Column(Integer, default=0)

    def __init__(self, chat_id, mode="nothing", time=0):
        self.chat_id = str(chat_id)  # ensure string
        self.mode = mode
        self.time = time


BlackListFilters.__table__.create(checkfirst=True)
BlackListMode.__table__.create(checkfirst=True)
BlSticker.__table__.create(checkfirst=True)

BLACKLIST_FILTER_INSERTION_LOCK = threading.RLock()

CHAT_BLACKLISTS = {}
CHAT_STICKER = {}


def add_to_blacklist(chat_id, trigger):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        blacklist_filt = BlackListFilters(str(chat_id), trigger)

        SESSION.merge(blacklist_filt)  # merge to avoid duplicate key issues
        SESSION.commit()
        CHAT_BLACKLISTS.setdefault(str(chat_id), set()).add(trigger)


def add_sticker(chat_id, sticker):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        blacklist_filt = BlSticker(str(chat_id), sticker)

        SESSION.merge(blacklist_filt)  # merge to avoid duplicate key issues
        SESSION.commit()
        CHAT_STICKER.setdefault(str(chat_id), set()).add(sticker)


def add_mode(chat_id, mode):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        mudd = SESSION.query(BlackListMode).get(str(chat_id))
        if not mudd:
            mudd = BlackListMode(str(chat_id))
        mudd.mode = mode
        SESSION.merge(mudd)  # merge to avoid duplicate key issues
        SESSION.commit()


def get_mode(chat_id):
    rules = SESSION.query(BlackListMode).get(str(chat_id))
    ret = "nothing"
    if rules:
        ret = rules.mode
    SESSION.close()
    return ret


def set_time(chat_id, time):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        mudd = SESSION.query(BlackListMode).get(str(chat_id))
        if not mudd:
            mudd = BlackListMode(str(chat_id))
        mudd.time = time


def get_time(chat_id):
    rules = SESSION.query(BlackListMode).get(str(chat_id))
    ret = 0
    if rules:
        ret = rules.time
    SESSION.close()
    return ret


def rm_from_blacklist(chat_id, trigger):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        blacklist_filt = SESSION.query(BlackListFilters).get((str(chat_id), trigger))
        if blacklist_filt:
            # sanity check
            if trigger in CHAT_BLACKLISTS.get(str(chat_id), set()):
                CHAT_BLACKLISTS.get(str(chat_id), set()).remove(trigger)

            SESSION.delete(blacklist_filt)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def remove_all_blacklist(chat_id):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        saved_bl = SESSION.query(BlackListFilters).filter(
            BlackListFilters.chat_id == str(chat_id)
        )
        if saved_bl:
            saved_bl.delete()
            SESSION.commit()
            CHAT_BLACKLISTS.pop(str(chat_id))


def rm_sticker(chat_id, sticker):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        blacklist_filt = SESSION.query(BlSticker).get((str(chat_id), sticker))
        if blacklist_filt:
            # sanity check
            if sticker in CHAT_STICKER.get(str(chat_id), set()):
                CHAT_STICKER.get(str(chat_id), set()).remove(sticker)

            SESSION.delete(blacklist_filt)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def get_chat_blacklist(chat_id):
    return CHAT_BLACKLISTS.get(str(chat_id), set())


def get_chat_sticker(chat_id):
    return CHAT_STICKER.get(str(chat_id), set())


def num_blacklist_filters():
    try:
        return SESSION.query(BlackListFilters).count()
    finally:
        SESSION.close()


def num_blacklist_chat_filters(chat_id):
    try:
        return (
            SESSION.query(BlackListFilters.chat_id)
            .filter(BlackListFilters.chat_id == str(chat_id))
            .count()
        )
    finally:
        SESSION.close()


def num_blacklist_filter_chats():
    try:
        return SESSION.query(func.count(distinct(BlackListFilters.chat_id))).scalar()
    finally:
        SESSION.close()


def __load_chat_blacklists():
    global CHAT_BLACKLISTS
    try:
        chats = SESSION.query(BlackListFilters.chat_id).distinct().all()
        for (chat_id,) in chats:  # remove tuple by ( ,)
            CHAT_BLACKLISTS[chat_id] = []

        all_filters = SESSION.query(BlackListFilters).all()
        for x in all_filters:
            CHAT_BLACKLISTS[x.chat_id] += [x.trigger]

        CHAT_BLACKLISTS = {x: set(y) for x, y in CHAT_BLACKLISTS.items()}

    finally:
        SESSION.close()


def __load_chat_stickers():
    global CHAT_STICKER
    try:
        chats = SESSION.query(BlSticker.chat_id).distinct().all()
        for (chat_id,) in chats:  # remove tuple by ( ,)
            CHAT_STICKER[chat_id] = []

        all_filters = SESSION.query(BlSticker).all()
        for x in all_filters:
            CHAT_STICKER[x.chat_id] += [x.sticker]

        CHAT_STICKER = {x: set(y) for x, y in CHAT_STICKER.items()}

    finally:
        SESSION.close()


__load_chat_blacklists()
__load_chat_stickers()
