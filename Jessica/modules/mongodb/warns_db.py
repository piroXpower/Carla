from .. import db

warns = db.warns

def warn_user(user_id, chat_id, reason=""):
  _warn = warns.find_one({"chat_id": chat_id, "user_id": user_id})
  if _warn:
    reasons = (_warn["reasons"]).append(reason)
    num_warns = _warn["num_warns"] + 1
  else:
    reasons = [reason]
    num_warns = 1
  warns.update_one({"chat_id": chat_id, "user_id": user_id}, {"$set": {"reasons": reasons, "num_warns": num_warns}}, upsert=True)
