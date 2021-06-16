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
        notes.update_one(
            {"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True
        )
