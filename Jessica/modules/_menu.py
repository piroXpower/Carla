import random

from telethon import Button, types

from Jessica.events import Cbot, Cinline

from . import db

plugins = [
    "admin",
    "afk",
    "approval",
    "chatbot",
    "filters",
    "greetings",
    "locks",
    "stickers",
    "rules",
    "song",
    "reporting",
    "quotly",
    "purges",
    "pin",
    "misc",
    "inline",
    "forcesub",
    "federations",
    "extras",
    "bans",
    "blocklist",
    "antiflood",
]
page = db.page

dps = [
    "https://telegra.ph/file/b596670c30be40cd2dc79.jpg",
    "https://telegra.ph/file/47630df50b92fc9de1138.jpg",
    types.InputDocument(
        id=6246529263399338896,
        access_hash=-5480756786203232946,
        file_reference=b"\x04W;~\xce\x00\x00\x05E\xd5\xd7\xce\x15i\x87'\x10Zv\xe1\xfa\xe2g\xd2\x83\xe1\xebA",
    ),
]
pm_caption = """
Hey! I am NekoChan, here to help you manage your groups! I perform most of the admin functions and make your group automated!
Hit /help to find out more about how to use me to my full potential.
You can checkout more about me via following buttons.
"""
pm_t = "Hello there! I'm NekoChan\nI'm a Telethon Based group management bot\n with a Much More! Have a look\nat the following for an idea of some of \nthe things I can help you with.\n\nMain commands available:\n/start : Starts me, can be used to check i'm alive or not.\n/help : PM's you this message.\n/help <module name> : PM's you info about that module.\n`/settings` : in PM: will send you your settings for all supported modules.\n~ in a group: will redirect you to pm, with all that chat's settings."


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
    if event.is_group:
        await event.reply(
            "Contact me in PM for help!",
            buttons=Button.url(
                "Click me for help!", "https://t.me/MissNeko_Bot?start=_help"
            ),
        )
    elif event.is_private:
        buttons = paginate_help(event, 0, plugins, "helpme")
        await event.reply(pm_t, buttons=buttons)


@Cinline(pattern=r"help_menu")
async def help_menu(event):
    buttons = paginate_help(event, 0, plugins, "helpme")
    await event.edit(pm_t, buttons=buttons)


def paginate_help(event, page_number, loaded_plugins, prefix):
    to_check = page.find_one({"id": event.sender_id})
    page.update_one({"id": event.chat_id}, {"$set": {"page": page_number}}, upsert=True)
    helpable_plugins = sorted(plugins)
    modules = [Button.inline(x, data=f"us_plugin_{x}") for x in helpable_plugins]
    return list(
        zip(
            modules[::3],
            modules[1::3],
            modules[2::3],
        )
    )
