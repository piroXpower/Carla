from telethon import Button

from Jessica.events import Cbot

from . import db

page = db.page

dp_1 = "https://telegra.ph/file/b596670c30be40cd2dc79.jpg"
pm_caption = """
Hey! I am Evie, here to help you manage your groups! I perform most of the admin functions and make your group automated!
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
        await event.reply(pm_caption, buttons=buttons, file=dp_1)
