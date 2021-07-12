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
                "report": True,
            }
        },
        upsert=True,
    )


def del_fed(fed_id):
    feds.delete_one({"fed_id": fed_id})
    fbans.delete_one({"fed_id": fed_id})


def transfer_fed(owner_id: int, user_id: int):
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


def user_demote_fed(fed_id, user_id: int):
    _fed = feds.find_one({"fed_id": fed_id})
    if _fed:
        fedadmins = _fed["fedadmins"]
        fedadmins.remove(user_id)
        feds.update_one(
            {"fed_id": fed_id}, {"$set": {"fedadmins": fedadmins}}, upsert=True
        )


def user_join_fed(fed_id, user_id: int):
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


def fban_user(fed_id, user_id: str, firstname, lastname, reason, time):
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


def get_fban_user(fed_id, user_id: str):
    _x_data = fbans.find_one({"fed_id": fed_id})
    if _x_data:
        _xx_data = _x_data.get("fbans")
        if _xx_data:
            __xxx_data = _xx_data.get(user_id)
            if __xxx_data:
                return True, __xxx_data[2], __xxx_data[3]
    return False, None, None


def search_user_in_fed(fed_id, user_id: int):
    _x = feds.find_one({"fed_id": fed_id})
    if _x:
        _admins = _x.get("fedadmins")
        if _admins and len(_admins) > 0:
            if user_id in _admins:
                return True
    return False


def user_feds_report(user_id: int):
    _x = feds.find_one({"owner_id": user_id})
    if _x:
        return _x["report"]
    return True


def set_feds_setting(user_id: int, mode):
    feds.update_one({"owner_id": user_id}, {"$set": {"report": mode}}, upsert=True)

def get_all_fed_admins(fed_id):
 _fed = feds.find_one({"fed_id", fed_id})
 x_admins = _fed["fedadmins"]
 x_owner = _fed["owner_id"]
 x_total = x_admins.append(x_owner)
 return x_total
