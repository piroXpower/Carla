from Jessica.modules import db

couples = db.couple
votes = db.votes_couple

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
    couples.update_one({"chat_id": chat_id}, {"$set": {"couple": lovers}}, upsert=True)

def update_vote(event_id: int, user_id: int, mode: str):
    _votes = votes.find_one({"event_id": event_id})
   if not _votes:
      users = []
   else:
      users = _votes["users"]
   if mode == "add":
     if not user_id in users:
      users.append(user_id)
   elif mode == "remove":
    if user_id in users:
      users.remove(user_id)
   votes.update_one({"event_id": event_id}, {"$set": {"users": users}}, upsert=True)
   
def voted(event_id: int, user_id: int):
 _votes = votes.find_one({"event_id": event_id})
 if not _votes:
      return False
 if user_id in _votes["users"]:
      return True
 return False
