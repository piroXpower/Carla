from sqlalchemy import Boolean, Column, String

from . import BASE, SESSION


class ChatBot(BASE):
    __tablename__ = "chatbot"
    chat_id = Column(String(14), primary_key=True)
    mode = Column(Boolean, default=True)

    def __init__(self, chat_id, mode=True):
        self.chat_id = chat_id
        self.mode = mode


ChatBot.__table__.create(checkfirst=True)


def set_chatbot_mode(chat_id: str, mode):
    bot = SESSION.query(ChatBot).get(str(chat_id))
    if bot:
        bot.mode = mode
    else:
        bot = ChatBot(chat_id, mode)
    SESSION.add(bot)
    SESSION.commit()


def chatbot_mode(chat_id: str):
    bot = SESSION.query(ChatBot).get(str(chat_id))
    if bot:
        return bot.mode
    return False
