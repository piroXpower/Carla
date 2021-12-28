import time

from telethon import Button

from .. import CMD_HELP, StartTime
from ..utils import Cbot, Cinline
from . import get_readable_time

plugins = [
    "Admin",
    "AFK",
    "Approval",
    "AI-Chatbot",
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
    "    Force-Sub   ",
    "Federations",
    "Extras",
    "Bans",
    "Blocklist",
    "Antiflood",
    "CAPTCHA",
    "Warnings",
]

dps = [
    "https://telegra.ph/file/aa142bd6faa787601cad9.jpg",
    "https://telegra.ph/file/8388d6c20d7f9be5d2b3e.jpg",
]
help_caption = """
Hey!. I am a group management bot, here to help you get around and keep the order in your groups!
I have lots of handy features, such as flood control, a warning system, a note keeping system, and even predetermined replies on certain keywords.

**Helpful commands:**
- `/start`: Starts me! You've probably already used this.
- `/help`: Sends this message; I'll tell you more about myself!

If you have any bugs or questions on how to use me, have a look at @NekoChan_Updates.
 All commands can be used with the following: `/!?`
"""
advanced_caption = """
Hey **{}**, .

I'm here to help you to manage your groups.
I have lots of handy features such as:
‣ Warning system
‣ Artificial intelligence
‣ Flood control system
‣ Note keeping system
‣ Filters keeping system
‣ Approvals and much more.

So what are you waiting for?
Add me in your groups and give me full rights to make me function well.
"""
about = """
**Aʙᴏᴜᴛ Mᴇ**

 Am Gʀᴏᴜᴘ Mᴀɴᴀɢᴇᴍᴇɴᴛ Bᴏᴛ Wʜᴏ Cᴀɴ Tᴀᴋᴇ Cᴀʀᴇ Oғ Yᴏᴜʀ Gʀᴏᴜᴘs Wɪᴛʜ Aᴜᴛᴏᴍᴀᴛᴇᴅ Rᴇɢᴜʟᴀʀ Aᴅᴍɪɴ Aᴄᴛɪᴏɴs! 

**Mʏ Sᴏғᴛᴡᴀʀᴇ Vᴇʀsɪᴏɴ:** 1.0.5

**Mʏ Dᴇᴠᴇʟᴏᴘᴇʀs:**
• `@piroXpower`
• `@BrayDenXD`

**Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ:** [Cʟɪᴄᴋ Hᴇʀᴇ](t.me/DeeCodeBots)
**Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ:** [Cʟɪᴄᴋ Hᴇʀᴇ](t.me/DeCodesupport)

__Aɴᴅ Fɪɴᴀʟʟʏ Sᴘᴇᴄɪᴀʟ Tʜᴀɴᴋs Oғ Gʀᴀᴛɪᴛᴜᴅᴇ Tᴏ Aʟʟ Mʏ Usᴇʀs Wʜᴏ Rᴇʟɪᴇᴅ Oɴ Mᴇ Fᴏʀ Mᴀɴᴀɢɪɴɢ Tʜᴇɪʀ Gʀᴏᴜᴘs , I Hᴏᴘᴇ Yᴏᴜ Wɪʟʟ Aʟᴡᴀʏs Lɪᴋᴇ Mᴇ ; Mʏ Dᴇᴠᴇʟᴏᴘᴇʀs Aʀᴇ Cᴏɴsᴛᴀɴᴛʟʏ Wᴏʀᴋɪɴɢ Tᴏ Iᴍᴘʀᴏᴠᴇ Mᴇ!__
"""
tc = """
**Tᴇʀᴍs Aɴᴅ Cᴏɴᴅɪᴛɪᴏɴs:**

- Oɴʟʏ Yᴏᴜʀ Usᴇʀ_Iᴅ Is Sᴛᴏʀᴇᴅ Fᴏʀ A Cᴏɴᴠᴇɴɪᴇɴᴛ Cᴏᴍᴍᴜɴɪᴄᴀᴛɪᴏɴ!
- Nᴏ Gʀᴏᴜᴘ Iᴅ Oʀ Iᴛs Mᴇssᴀɢᴇs Aʀᴇ Sᴛᴏʀᴇᴅ , Wᴇ Rᴇsᴘᴇᴄᴛ Eᴠᴇʀʏᴏɴᴇ's Pʀɪᴠᴀᴄʏ.
- Mᴇssᴀɢᴇs Bᴇᴛᴡᴇᴇɴ Bᴏᴛ Aɴᴅ Yᴏᴜ Is Oɴʟʏ IɴFʀᴏɴᴛ Oғ Yᴏᴜʀ Eʏᴇs Aɴᴅ Tʜᴇʀᴇ Is Nᴏ BᴀᴄᴋUsᴇ Oғ Iᴛ.
- Wᴀᴛᴄʜ Yᴏᴜʀ Gʀᴏᴜᴘ , Iғ Sᴏᴍᴇᴏɴᴇ Is Sᴘᴀᴍᴍɪɴɢ Yᴏᴜʀ Gʀᴏᴜᴘ , Yᴏᴜ Cᴀɴ Usᴇ Tʜᴇ Rᴇᴘᴏʀᴛ Fᴇᴀᴛᴜʀᴇ Oғ Yᴏᴜʀ Tᴇʟᴇɢʀᴀᴍ Cʟɪᴇɴᴛ.
- Dᴏ Nᴏᴛ Sᴘᴀᴍ Cᴏᴍᴍᴀɴᴅs , Bᴜᴛᴛᴏɴs , Oʀ Aɴʏᴛʜɪɴɢ Iɴ Bᴏᴛ Pᴍ

𝙉𝙊𝙏𝙀: Tᴇʀᴍs Aɴᴅ Cᴏɴᴅɪᴛɪᴏɴs Mɪɢʜᴛ Cʜᴀɴɢᴇ Aɴʏᴛɪᴍᴇ.

**Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ:** [Cʟɪᴄᴋ Hᴇʀᴇ](t.me/DeeCodeBots)
**Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ:** [Cʟɪᴄᴋ Hᴇʀᴇ](t.me/DeCodesupport)
"""
start_buttons = [
    [Button.url("Add to your Group ➕", "https://t.me/DeCodeManagerBot?startgroup=true")],
    [
        Button.inline("Advanced ⭐", data="soon"),
        Button.url("Gban Logs 🌐", "https://t.me/vc_protectOp"),
    ],
    [Button.inline("Help and commands ❓", data="help_menu")],
]


p = """
Hello {}, I'm KingBot,
I am a full-fledged group management bot with some fun extras ;)

I can do a variety of things, most common of em are:
- Restrict users with ban permissions.
- Greet users with media + text and buttons, with proper formatting.
- Restrict users who flood your chat using my anti-flood module.
- Warn users according to the options set and restrict em accordingly.
- Save notes and filters with proper formatting and reply markup.

Theres even more! this is just the tip of the iceberg. Do note I need
to be promoted with proper admin permissions to function properly. 
Else I won't be able to function as said.

Click on help to learn more!
"""


@Cbot(pattern="^/start(@DecodeManagerBot)?$")
async def start(e):
    if e.is_group or e.is_channel:
        await e.reply(
            "Well I'm alive!\n**Working since:** {}".format(
                get_readable_time(time.time() - StartTime)
            )
        )
    elif e.is_private:
        await e.respond(
            p.format(e.sender.first_name),
            buttons=start_buttons,
        )


@Cbot(pattern="^/help ?(.*)")
async def help(event):
    if event.is_group:
        buttons = [
            [Button.url("❔ Help", "https://t.me/kingXlBot?start=_help")],
        ]
        await event.reply(
            "Contact me in PM to get the list of possible commands.",
            buttons=buttons,
        )
    elif event.is_private:
        buttons = paginate_help()
        await event.reply(help_caption, buttons=buttons)


@Cbot(pattern="^/start _help")
async def st_help(e):
    buttons = paginate_help()
    await e.respond(help_caption, buttons=buttons)


@Cinline(pattern=r"help_menu")
async def help_menu(event):
    buttons = paginate_help()
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


def paginate_help():
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
    modulo_page = 0 % 1
    pairs = pairs[modulo_page * 8 : 8 * (modulo_page + 1)] + [
        (Button.inline("Back", data="soon"),)
    ]
    return pairs


@Cinline(pattern="soon")
async def soon(event):
    buttons = [
        [Button.url("Configuration Tutorial", "https://t.me/Hindi_English_Chatting_Group/11850778")],
        [
            Button.inline("About Me", data="me_detail"),
            Button.inline("Commands", data="help_menu"),
        ],
        [Button.inline("Terms and Conditions", data="t&c")],
    ]
    await event.edit(
        advanced_caption.format(event.sender.first_name),
        buttons=buttons,
    )


@Cinline(pattern="me_detail")
async def me(e):
    buttons = Button.inline("Back", data="soon")
    await e.edit(about, buttons=buttons, link_preview=False)


@Cinline(pattern="t&c")
async def t_c(e):
    buttons = Button.inline("Back", data="soon")
    await e.edit(tc, buttons=buttons, link_preview=False)


@Cbot(pattern="^/privacy$")
async def provacy_eee___(e):
    if not e.is_private:
        return
    b = [
        [Button.inline("Privacy Policy", data="pp")],
        [
            Button.inline("Retrieve Data", data="rrdata"),
            Button.inline("Delete Data", data="deld"),
        ],
        [Button.inline("Cancel", data="pcancel")],
    ]
    await e.respond(
        "Select one of the below options for more information about how the bot handles your privacy.",
        buttons=b,
    )


@Cinline(pattern="pp")
async def pp_cb(e):
    xp = """
**Our contact details**
**Name:** king bot
**Telegram:** https://t.me/decodeSupport

The bot has been made to **protect** and **preserve** privacy as best as possible.
The proper functioning of the bot is defined as the data required for all the commands in the /help to work as expected.

Our privacy policy may change from time to time. If we make any material changes to our policies, we will place a prominent notice on https://t.me/NekoChan_Updates.
"""
    b = [
        [Button.inline("What information we collect", data="pcollect")],
        [Button.inline("Why we collect it", data="pdatawhy")],
        [Button.inline("What we do", data="pwwd")],
        [Button.inline("What we DO NOT do", data="wwdnd")],
        [Button.inline("Rights to process", data="rrtd")],
    ]
    await e.edit(xp, buttons=b, link_preview=False)


@Cinline(pattern="pcollect")
async def p_collect_cb_(e):
    xp = """
**The type of personal information we collect**

We currently collect and process the following information:
    • Telegram UserID, firstname, lastname, username (Note: These are your public telegram details. We do not know your "real" details.)
    • Settings or configurations as set through any commands (For example, welcome settings, notes, filters, etc)
"""
    b = [
        [Button.inline("• What information we collect •", data="pcollect")],
        [Button.inline("Why we collect it", data="pdatawhy")],
        [Button.inline("What we do", data="pwwd")],
        [Button.inline("What we DO NOT do", data="wwdnd")],
        [Button.inline("Rights to process", data="rrtd")],
        [Button.inline("Back", data="pp")],
    ]
    await e.edit(xp, buttons=b)
