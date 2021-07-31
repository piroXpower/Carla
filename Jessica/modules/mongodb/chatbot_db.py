from .. import db

chatbot = db.chatbot


def set_chatbot(chat_id: int, mode):
    chatbot.update_one({"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True)


def is_chat(chat_id: int):
    chat_s = chatbot.find_one({"chat_id": chat_id})
    if chat_s:
        return chat_s["mode"]
    return False
