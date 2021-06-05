from sqlalchemy import Boolean, Column, String

from . import BASE, SESSION


class LOCKS(BASE):
    __tablename__ = "locks"
    chat_id = Column(String(14), primary_key=True)
    media = Column(Boolean, default=False)
    audio = Column(Boolean, default=False)
    video = Column(Boolean, default=False)
    sticker = Column(Boolean, default=False)
    gif = Column(Boolean, default=False)
    inline = Column(Boolean, default=False)
    all = Column(Boolean, default=False)
    emojigame = Column(Boolean, default=False)
    phone = Column(Boolean, default=False)
    photo = Column(Boolean, default=False)
    url = Column(Boolean, default=False)
    location = Column(Boolean, default=False)
    invitelink = Column(Boolean, default=False)
    forward = Column(Boolean, default=False)
    document = Column(Boolean, default=False)
    contact = Column(Boolean, default=False)
    command = Column(Boolean, default=False)
    button = Column(Boolean, default=False)
    bot = Column(Boolean, default=False)

    def __init__(
        self,
        chat_id,
        media,
        audio,
        video,
        sticker,
        gif,
        inline,
        all,
        emojigame,
        phone,
        photo,
        url,
        location,
        invitelink,
        forward,
        document,
        contact,
        command,
        button,
        bot,
    ):
        self.chat_id = chat_id
        self.media = media
        self.audio = audio
        self.video = video
        self.sticker = sticker
        self.gif = gif
        self.inline = inline
        self.all = all
        self.emojigame = emojigame
        self.phone = phone
        self.photo = photo
        self.url = url
        self.location = location
        self.invitelink = invitelink
        self.forward = forward
        self.document = document
        self.contact = contact
        self.command = command
        self.button = button
        self.bot = bot


LOCKS.__table__.create(checkfirst=True)


def add_lock(
    chat_id,
    media=False,
    audio=False,
    video=False,
    sticker=False,
    gif=False,
    inline=False,
    all=False,
    emojigame=False,
    phone=False,
    photo=False,
    url=False,
    location=False,
    invitelink=False,
    forward=False,
    document=False,
    contact=False,
    command=False,
    button=False,
    bot=False,
):
    curr = SESSION.query(LOCKS).get(str(chat_id))
    if curr:
        if media:
            curr.media = True
        if audio:
            curr.audio = True
        if video:
            curr.video = True
        if sticker:
            curr.sticker = True
        if gif:
            curr.gif = True
        if inline:
            curr.inline = True
        if all:
            curr.all = True
        if emojigame:
            curr.emojigame = True
        if phone:
            curr.phone = True
        if photo:
            curr.photo = True
        if url:
            curr.url = True
        if location:
            curr.location = True
        if invitelink:
            curr.invitelink = True
        if forward:
            curr.forward = True
        if document:
            curr.document = True
        if contact:
            curr.contact = True
        if command:
            curr.command = True
        if button:
            curr.button = True
        if bot:
            curr.bot = True
    else:
        curr = LOCKS(
            chat_id,
            media,
            audio,
            video,
            sticker,
            gif,
            inline,
            all,
            emojigame,
            phone,
            photo,
            url,
            location,
            invitelink,
            forward,
            document,
            contact,
            command,
            button,
            bot,
        )
    SESSION.add(curr)
    SESSION.commit()


def remove_lock(
    chat_id,
    media=True,
    audio=True,
    video=True,
    sticker=True,
    gif=True,
    inline=True,
    all=True,
    emojigame=True,
    phone=True,
    photo=True,
    url=True,
    location=True,
    invitelink=True,
    forward=True,
    document=True,
    contact=True,
    command=True,
    button=True,
    bot=True,
):
    curr = SESSION.query(LOCKS).get(str(chat_id))
    if curr:
        if media:
            curr.media = False
        if audio:
            curr.audio = False
        if video:
            curr.video = False
        if sticker:
            curr.sticker = False
        if gif:
            curr.gif = False
        if inline:
            curr.inline = False
        if all:
            curr.all = False
        if emojigame:
            curr.emojigame = False
        if phone:
            curr.phone = False
        if photo:
            curr.photo = False
        if url:
            curr.url = False
        if location:
            curr.location = False
        if invitelink:
            curr.invitelink = False
        if forward:
            curr.forward = False
        if document:
            curr.document = False
        if contact:
            curr.contact = False
        if command:
            curr.command = False
        if button:
            curr.button = False
        if bot:
            curr.bot = False
    else:
        curr = LOCKS(
            chat_id,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        )
    SESSION.add(curr)
    SESSION.commit()
