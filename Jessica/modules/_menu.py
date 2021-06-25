import random

from telethon import Button, types

from Jessica.events import Cbot

from . import db

page = db.page

dps = [
    "https://telegra.ph/file/b596670c30be40cd2dc79.jpg",
    "https://telegra.ph/file/47630df50b92fc9de1138.jpg",
    types.InputDocument(id=6246529263399338896, access_hash=-5480756786203232946, file_reference=b"\x04W;~\xce\x00\x00\x05E\xd5\xd7\xce\x15i\x87'\x10Zv\xe1\xfa\xe2g\xd2\x83\xe1\xebA")
]
pm_caption = """
Hey! I am NekoChan, here to help you manage your groups! I perform most of the admin functions and make your group automated!
Hit /help to find out more about how to use me to my full potential.
You can checkout more about me via following buttons.
"""


@Cbot(pattern="^/start$")
async def start(event):
    if event.is_group or event.is_channel:
        await event.reply("Hi there, I'm online ^_^")
    elif event.is_private:
        buttons = [
            [
                Button.inline("Advanced", data="soon"),
                Button.inline("Commands", data="help_menu"),
            ],
            [
                Button.url(
                    "Add Me To Your Group!", "t.me/missneko_bot?startgroup=true"
                ),
            ],
        ]
        await event.respond(pm_caption, buttons=buttons, file=random.choice(dps))


@Cbot(pattern="^/help ?(.*)")
async def help(event):
    print("#")
