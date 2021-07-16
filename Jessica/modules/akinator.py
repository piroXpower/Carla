from akinator import Akinator
from telethon import Button

from ..events import Cbot

q = Akinator()
buttons = [
    [
        Button.inline("Yes", data="aki_yes"),
        Button.inline("No", data="aki_no"),
        Button.inline("Probably", data="aki_probably"),
    ],
    [
        Button.inline("I don't Know", data="aki_idk"),
        Button.inline("Probably not", data="aki_probably_not"),
    ],
    [Button.inline("Go Back", data="aki_back")],
]

db = {}


@Cbot(pattern="^/akinator ?(.*)")
async def akinator(e):
    f = await e.respond("Loading...")
    first_q = q.start_game()
    db[e.sender_id] = first_q
    await f.edit(first_q, buttons=buttons)


@Cbot(pattern="aki_yes")
async def aki_yes_(e):
    p = q.answer("Yes")
    await e.edit(p)
