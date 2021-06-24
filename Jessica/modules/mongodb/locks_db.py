from Jessica.modules import db
locks = locks.db

def add_lock(chat_id, type)
 _locks = locks.find_one({"chat_id": chat_id})
 if _locks:
   _lock = _locks["locked"]
 else:
   _lock = []
 _lock.append(type)
 new_lock = list(set(_lock))
 locks.update_one({"chat_id": chat_id}, {"$set": {"locked": new_lock}}, upsert=True)
 
def get_locks(chat_id):
 _locks = locks.find_one({"chat_id": chat_id})
 if _locks:
   return _locks["locked"]
 return None
