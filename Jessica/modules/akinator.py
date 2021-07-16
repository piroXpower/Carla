import asyncio

from akinator import Akinator
from telethon import Button

from ..events import Cbot, Cinline

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
    db[e.sender_id] = 1
    await f.edit(first_q, buttons=buttons)


@Cinline(pattern="aki_yes")
async def aki_yes_(e):
    db[e.sender_id] = db[e.sender_id] + 1
    p = q.answer("Yes")
    if db[e.sender_id] > 40:
        q.win()
        p = q.first_guess
        return await e.edit(str(p))
    await asyncio.sleep(1)
    await e.edit(p, buttons=buttons)


@Cinline(pattern="aki_no")
async def aki_no_(e):
    db[e.sender_id] = db[e.sender_id] + 1
    p = q.answer("No")
    if db[e.sender_id] > 40:
        q.win()
        p = q.first_guess
        return await e.edit(str(p))
    await asyncio.sleep(1)
    await e.edit(p, buttons=buttons)


@Cinline(pattern="aki_probably")
async def aki_probably(e):
    db[e.sender_id] = db[e.sender_id] + 1
    p = q.answer("Probably")
    if db[e.sender_id] > 40:
        q.win()
        p = q.first_guess
        return await e.edit(str(p))
    await asyncio.sleep(1)
    await e.edit(p, buttons=buttons)


@Cinline(pattern="aki_idk")
async def aki_idk(e):
    db[e.sender_id] = db[e.sender_id] + 1
    p = q.answer("I don't Know")
    if db[e.sender_id] > 40:
        q.win()
        p = q.first_guess
        return await e.edit(str(p))
    await asyncio.sleep(1)
    await e.edit(p, buttons=buttons)


@Cinline(pattern="aki_probably_not")
async def aki_probably_not_(e):
    p = q.answer("Probably not")
    db[e.sender_id] = db[e.sender_id] + 1
    if db[e.sender_id] > 40:
        q.win()
        p = q.first_guess
        return await e.edit(str(p))
    await asyncio.sleep(1)
    await e.edit(p, buttons=buttons)


@Cinline(pattern="aki_back")
async def aki_back(e):
    if db[e.sender_id] == 1:
        return await e.answer(
            "This is the first question, You can't go back any further."
        )
    db[e.sender_id] = db[e.sender_id] + 1
    p = q.back()
    await asyncio.sleep(1)
    await e.edit(p, buttons=buttons)
