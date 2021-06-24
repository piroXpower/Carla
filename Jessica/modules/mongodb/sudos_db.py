from Jessica.modules import db

sudo_m = db.sudo_m


def add_sudo(user_id: int, name: str):
    sudos = sudo_m.find_one({"type": "staffs"})
    if sudos:
        sudos = sudos["sudo"]
        sudos[user_id] = name
    else:
        sudos = {}
        sudos[user_id] = name
    sudo_m.update_one({"type": "staffs"}, {"$set": {"sudo": devs}}, upsert=True)


def add_dev(user_id: int, name: str):
    devs = sudo_m.find_one({"type": "staffs"})
    if devs:
        devs = devs["dev"]
        devs[user_id] = name
    else:
        devs = {}
        devs[user_id] = name
    sudo_m.update_one({"type": "staffs"}, {"$set": {"dev": devs}}, upsert=True)
