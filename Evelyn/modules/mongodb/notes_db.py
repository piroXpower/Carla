from Evelyn.modules import db

notes = db.notes


def save_note(chat_id, name, note):
    _note = notes.find_one({"chat_id": chat_id})
    if not _note:
        _notes = {}
    else:
        _notes = _note["notes"]
    _notes[name] = note
    notes.update_one({"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True)
