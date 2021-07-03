import random

from telethon import Button

from Jessica import CMD_HELP
from Jessica.events import Cbot, Cinline

from . import db

plugins = [
    "Admin",
    "AFK",
    "Approval",
    "Chatbot",
    "Filters",
    "Greetings",
    "Locks",
    "Stickers",
    "Rules",
    "Song",
    "Reports",
    "Quotly",
    "Purges",
    "Pin",
    "Misc",
    "Inline",
    "Forcesubscribe",
    "Federations",
    "Extras",
    "Bans",
    "Blocklist",
    "Antiflood",
    "CAPTCHA",
    "Warnings",
]
page = db.page

dps = [
    "https://telegra.ph/file/c6e1b8dffef90de602f52.jpg",
    "https://telegra.ph/file/75bf845ca6c731e7f0dc3.jpg",
]
pm_caption = """
Hey! I am NekoChan, here to help you manage your groups! I perform most of the admin functions and make your group automated!
Hit /help to find out more about how to use me to my full potential.
You can checkout more about me via following buttons.
"""
help_caption = """
Hey! My name is NekoChan. I am a group management bot, here to help you get around and keep the order in your groups!
I have lots of handy features, such as flood control, a warning system, a note keeping system, and even predetermined replies on certain keywords.

**Helpful commands:
- /start: Starts me! You've probably already used this.
- /help: Sends this message; I'll tell you more about myself!

If you have any bugs or questions on how to use me, have a look at @NekoChan_Updates.
 All commands can be used with the following: / ! ?
"""
advanced_caption = """
Hey! I am NekoChan, here to help you manage your groups! I perform most of the admin functions and make your group automated!

@NekoChan_Updates for updates channel.
@NekoChan_Support in for support group.

You can checkout more about me via following buttons.
"""
about = """
**About Me**
 
My name is NekoChan, A group management bot who can take care of your groups with automated regular admin actions! 
 
**My Software Version:** 1.0.4
 
**My Developers:**
• `@RoseLoverX`
• `@Itz_RexModz`
• `@Anukili`
 
**Updates Channel:** [Click Here](t.me/nekochan_updates)
**Support Chat:** [Click Here](t.me/nekochan_support)
 
__And finally special thanks of gratitude to all my users who relied on me for managing their groups, I hope you will always like me; My developers are constantly working to improve me!__
"""
tc = """
**Terms and Conditions:**

- Only your user_id is stored for a convenient communication!
- No group ID or it's messages are stored, we respect everyone's
  privacy.
- Messages between Bot and you is only infront of your eyes and 
  there is no backuse of it.
- Watch your group, if someone is spamming your group, you can 
  use the report feature of your Telegram Client.
- Do not spam commands, buttons, or anything in bot PM.

**NOTE:** __Terms and Conditions might change anytime__

**Updates Channel:** [Click Here](t.me/nekochan_updates)
**Support Chat:** [Click Here](t.me/nekochan_support)
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
    if event.is_group:
        await event.reply(
            "Contact me in PM for help!",
            buttons=Button.url(
                "Click me for help!", "https://t.me/MissNeko_Bot?start=_help"
            ),
        )
    elif event.is_private:
        buttons = paginate_help(event, 0, plugins, "helpme")
        await event.reply(help_caption, buttons=buttons)


@Cinline(pattern=r"help_menu")
async def help_menu(event):
    buttons = paginate_help(event, 0, plugins, "helpme")
    await event.edit(help_caption, buttons=buttons)


@Cinline(pattern=r"us_plugin_(.*)")
async def us_0(event):
    pl_name = (event.pattern_match.group(1)).decode()
    try:
        pl_help = CMD_HELP[pl_name][1]
    except KeyError:
        pl_help = "The help menu for this module will be provided soon!"
    await event.edit(
        pl_help,
        buttons=[
            Button.inline("Home", data="soon"),
            Button.inline("Back", data="help_menu"),
        ],
    )


def paginate_help(event, page_number, loaded_plugins, prefix):
    to_check = page.find_one({"id": event.sender_id})
    page.update_one({"id": event.chat_id}, {"$set": {"page": page_number}}, upsert=True)
    helpable_plugins = sorted(plugins)
    modules = [
        Button.inline(x, data=f"us_plugin_{x.lower()}") for x in helpable_plugins
    ]
    pairs = list(
        zip(
            modules[::3],
            modules[1::3],
            modules[2::3],
        )
    )
    modulo_page = page_number % 1
    pairs = pairs[modulo_page * 8 : 8 * (modulo_page + 1)] + [
        (Button.inline("Back", data="soon"),)
    ]
    return pairs


@Cinline(pattern="soon")
async def soon(event):
    buttons = [
        [Button.url("Configuration Tutorial", "https://t.me/NekoChan_Updates/13")],
        [
            Button.inline("About Me", data="me_detail"),
            Button.inline("Commands", data="help_menu"),
        ],
        [Button.inline("Terms and Conditions", data="t&c")],
    ]
    await event.edit(advanced_caption, buttons=buttons)


@Cinline(pattern="me_detail")
async def me(e):
    buttons = Button.inline("Back", data="soon")
    await e.edit(about, buttons=buttons, link_preview=False)


@Cinline(pattern="t&c")
async def t_c(e):
    buttons = Button.inline("Back", data="soon")
    await e.edit(tc, buttons=buttons, link_preview=False)


