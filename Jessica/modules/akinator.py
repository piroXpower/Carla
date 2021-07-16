from akinator import Akinator
from telethon import Button

from ..events import Cbot

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


@Cbot(pattern="^/akinator ?(.*)")
async def akinator(e):
    await e.respond("Loading...")
    q = Akinator()
    first_q = q.start_game()
    await e.respond(first_q, buttons=buttons)
