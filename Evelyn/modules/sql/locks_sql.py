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


def change_mode(
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
