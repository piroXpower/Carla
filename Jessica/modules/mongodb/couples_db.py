from Jessica.modules import db
couples = db.couples


def get_couple(chat_id: int, date: str):
    _lovers = couples.find_one({"chat_id": chat_id})
    if not _lovers:
      lovers = {}
    else:
      lovers = _lovers["couple"]
    if date in lovers:
        return lovers[date]
    else:
        return False


def save_couple(chat_id: int, date: str, couple: dict):
    _lovers = couples.find_one({"chat_id": chat_id})
    if not _lovers:
      lovers = {}
    else:
      lovers = _lovers["couple"]
    lovers[date] = couple
    couples.update_one(
        {"chat_id": chat_id}, {"$set": {"couple": lovers}}, upsert=True
    )
