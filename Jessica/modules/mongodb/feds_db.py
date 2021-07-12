from .. import db

feds = db.feds
fbans = db.fbans


def new_fed(owner_id: int, fed_id, fedname):
    feds.update_one(
        {"owner_id": owner_id},
        {
            "$set": {
                "fed_id": fed_id,
                "fedname": fedname,
                "fedadmins": [],
                "flog": None,
                "chats": [],
            }
        },
        upsert=True,
    )


def del_fed(fed_id):
    feds.delete_one({"fed_id": fed_id})


def transfer_fed(owner_id, user_id):
    _fed = feds.find_one({"owner_id": owner_id})
    if _fed:
        feds.update_one(
            {"fed_id": _fed["fed_id"]}, {"$set": {"owner_id": user_id}}, upsert=True
        )


def rename_fed(fed_id, fname):
    _fed = feds.find_one({"fed_id": fed_id})
    if _fed:
        feds.update_one({"fed_id": fed_id}, {"$set": {"fedname": fname}}, upsert=True)


def chat_join_fed(fed_id, chat_id: int):
    _fed = feds.find_one({"fed_id": fed_id})
    if _fed:
        chats = _fed["chats"]
        chats.append(chat_id)
        feds.update_one({"fed_id": fed_id}, {"$set": {"chats": chats}}, upsert=True)


def user_demote_fed(fed_id, user_id):
    _fed = feds.find_one({"fed_id": fed_id})
    if _fed:
        fedadmins = _fed["fedadmins"]
        fedadmins.remove(user_id)
        feds.update_one(
            {"fed_id": fed_id}, {"$set": {"fedadmins": fedadmins}}, upsert=True
        )


def user_join_fed(fed_id, user_id):
    _fed = feds.find_one({"fed_id": fed_id})
    if _fed:
        fedadmins = _fed["fedadmins"]
        fedadmins.append(user_id)
        feds.update_one(
            {"fed_id": fed_id}, {"$set": {"fedadmins": fedadmins}}, upsert=True
        )


def chat_leave_fed(fed_id, chat_id):
    _fed = feds.find_one({"fed_id": fed_id})
    if _fed:
        chats = _fed["chats"]
        chats.remove(chat_id)
        feds.update_one({"fed_id": fed_id}, {"$set": {"chats": chats}}, upsert=True)


def fban_user(fed_id, user_id, firstname, lastname, reason, time):
    _fban = fbans.find_one({"fed_id": fed_id})
    if _fban:
        f_bans = _fban["fbans"]
    else:
        f_bans = {}
    f_bans[user_id] = [firstname, lastname, reason, time]
    fbans.update_one({"fed_id": fed_id}, {"$set": {"fbans": f_bans}}, upsert=True)


def unfban_user(fed_id, user_id):
    _fban = fbans.find_one({"fed_id": fed_id})
    if _fban:
        f_bans = _fban["fbans"]
    else:
        f_bans = {}
    if f_bans[user_id]:
        del f_bans[user_id]
    fbans.update_one({"fed_id": fed_id}, {"$set": {"fbans": f_bans}}, upsert=True)


def super_fban(user_id):
    print("soon")


def get_user_owner_fed_full(owner_id):
    _all_feds = feds.find_one({"owner_id": owner_id})
    if _all_feds:
        return _all_feds["fed_id"], _all_feds["fedname"]
    return None


def search_fed_by_id(fed_id):
    _x_fed = feds.find_one({"fed_id": fed_id})
    if _x_fed:
        return _x_fed
    return None


def get_chat_fed(chat_id):
    _x = feds.find({})
    for x in _x:
        if chat_id in x["chats"]:
            return_able = x["fed_id"]
            if len(return_able) == 0:
                return None
            return return_able
    return None
