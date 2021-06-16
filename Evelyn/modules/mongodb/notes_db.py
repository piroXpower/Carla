from Evelyn.modules import db

notes = db.notes

def save_note(chat_id, name, note):
    name = name.lower().strip()
    _note = notes.find_one({"chat_id": chat_id})
    if not _note:
        _notes = {}
    else:
        _notes = _note["notes"]
    _notes[name] = note
    notes.update_one({"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True)


def delete_note(chat_id, name):
    name = name.strip().lower()
    _note = notes.find_one({"chat_id": chat_id})
    if not _note:
        _notes = {}
    else:
        _notes = _note["notes"]
    if name in _notes:
        del _notes[name]
        notes.update_one({"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True)


def get_note(chat_id, name):
    name = name.strip().lower()
    _note = notes.find_one({"chat_id": chat_id})
    if not _note:
        _notes = {}
    else:
        _notes = _note["notes"]
    if name in _notes:
        return _notes[name]
    return False


def get_all_notes(chat_id):
    _note = notes.find_one({"chat_id": chat_id})
    if _note:
        return _note["notes"]
    return None


def delete_all_notes(chat_id):
    _note = notes.find_one({"chat_id": chat_id})
    if note:
        notes.delete_one({"chat_id": chat_id})
        return True
    return False
