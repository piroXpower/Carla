from . import db

rules = db.rules


def set_rules(chat_id: int, rules: str):
    rules.update_one({"chat_id": chat_id}, {"$set": {"rules": rules}}, upsert=True)


def get_rules(chat_id: int):
    _rules = rules.find_one({"chat_id": chat_id})
    if _rules:
        return _rules["rules"]
    return False


def del_rules(chat_id: int):
    _rules = rules.find_one({"chat_id": chat_id})
    if _rules:
        rules.delete_one({"chat_id": chat_id})
