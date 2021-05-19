import re
from math import ceil

from telethon import Button, custom, events

from Elsie import CMD_LIST, tbot
from Elsie.events import Cbot

from . import db

pagenumber = db.pagenumber

string = "Contact me in PM for help!"
n_button = [
    Button.inline("Example usage", data="n_eu"),
    Button.inline("Formatting", data="formatting"),
], [Button.inline("Back", data="go_back")]
f_button = (
    [
        Button.inline("Fed Admin Commands", data="f_ad"),
        Button.inline("Fed Owner Commands", data="f_ow"),
    ],
    [Button.inline("User Commands", data="f_us")],
    [Button.inline("Back", data="go_back")],
)
c_button = Button.inline("Back", data="go_back")
bl_button = [Button.inline("Blocklist Command Examples", data="bl_cmd")], [
    Button.inline("Back", data="go_back")
]
# Soon
a_about_str = """
**About me:**
I am **Elsie**, a python based Telegram Group Management bot

My developers:
**• @RoseLoverX**

Thanks to My Sudo & Support users who makes me usable for you!

**Updates channel: @ElsieNews**
**Support Chat: @ElsieSupport**
"""
about_str = """
**Elsie bot - A bot to manage your groups with additional features**
Here's the basic help regarding use of Nidhi.

Almost all modules usage defined in the help menu, checkout by sending `/help`

Report error/bugs here **@ElsieSupport**.
"""

start_str = """
Hi **{}**
I'm **Elsie**, A bot to manage your chats when you're offline.
What can i do?
I can do lot of cool stuffs, here's a short list:
 • I can **Restrict** user.
 • I can **greets** users with customizable welcome messages and even set a group's rules.
 • I have an advanced **anti-flood** system.
 • I can warn users until they reach max warns, with each predefined actions such as ban, mute, kick, etc.
 • I have a **note** keeping system, **blacklists**, and even pre determined replies on certain keywords.
 
Checkout Full Help menu by sending `/help` To know about my modules and usage.
"""
tandc = """
**Terms and Conditions:**

• Only your first name, last name(if any) and username(if any) is stored.
• No group ID or it's messages are stored, We respect everyone's privacy.
• Don't spam commands, buttons, or anything in bot PM, if we found anyone doing than he will probhited to use Elsie permanently.
• Messages between Bot & you is only infront of your eyes and there is no backuse of it..
• NSFW will get permanent global ban in Elsie which never removes, report spammers here -> **@ElsieSupport**.

**NOTE:** __Terms and Conditions will be change anytime__.

**Join @ElsieNews for Updates.**
**Join @ElsieSupport to get answer of yours questions.**
"""
help_str = """
Hello there! My name is **Elsie**.
A group management bot with a few fun extras! Have a look at the following for an idea of some of the things I can help you with.
Main commands available:
 • /start : Starts me, can be used to check i'm alive or no...
 • /help : PM's you this message.
 • /help `<module name>` : PM's you info about that module.
 • /support : Sends a request to Bot Staff to help you regarding your issue. (Groups only.)
 
Need help? head to @ElsieSupport
 
Click on the buttons below to get documentation about specific modules!
"""

captcha = """
**CAPTCHA**

Some chats get a lot of users joining just to spam. This could be because they're trolls, or part of a spam network.
To slow them down, you could try enabling CAPTCHAs. New users joining your chat will be required to complete a test to confirm that they're real people.'

**Admin commands:**
- /captcha `<yes/no/on/off>`: All users that join will need to solve a CAPTCHA. This proves they aren't a bot!
- /captchamode `<button/math/text>`: Choose which CAPTCHA type to use for your chat.
- /captcharules `<yes/no/on/off>`: Require new users accept the rules before being able to speak in the chat.
- /captchatime `<Xw/d/h/m>`: Unmute new users after X time. If a user hasn't solved the CAPTCHA yet, they get automatically unmuted after this period.
- /captchakick `<yes/no/on/off>`: Kick users that haven't solved the CAPTCHA.
- /captchakicktime `<Xw/d/h/m>`: Set the time after which to kick CAPTCHA'd users.
- /setcaptchatext `<text>`: Customise the CAPTCHA button.
- /resetcaptchatext: Reset the CAPTCHA button to the default text.

**Examples:**
- Enable CAPTCHAs
-> `/captcha on`
- Change the CAPTCHA mode to text.
-> `/captchamode text`
- Enable CAPTCHA rules, forcing users to read the rules before being allowed to speak.
-> `/captcharules on`
NOTE:
For CAPTCHAs to be enabled, you MUST have enabled welcome messages. If you disable welcome messages, CAPTCHAs will also stop.
"""

example = """
**Example Usage**

Notes can seem quite complicated; so here are some examples, so you can get some inspiration.

**Examples:**
- Saving a note. Now, anyone using #test or `/get test` will see this message. To save an image, gif, sticker, or any other kind of data, simply reply to that message
-> `/save test This is a fancy note!`
- To retrieve a note without formatting, add noformat after the get command. This will retrieve the note with no formatting, allowing you to copy and edit it.
-> `/get notename noformat`
- You can also link notes through notebuttons. To do this, simply use the notename as the URL:
-> `/save note This is a note [With a button](buttonurl://#anothernote)
- To save an admin-only note:
-> `/save example This note will only be opened by admins {admin}`
- To send all notes to the user's PM:
-> `/privatenotes on`
- To send a single note to user's PM, add a {private} tag to your note:
-> `/save test This is a note that always goes to PM {private}`
- If you've enabled privatenotes, but have one note that you don't want to go to PM:
-> `/save test This is a note that always goes to groups {noprivate}`
"""

welcome = """
**Greetings**

Give your members a warm welcome with the greetings module! Or a sad goodbye... Depends!

**Admin commands:**
- /welcome <yes/no/on/off>: Enable/disable welcomes messages.
- /goodbye <yes/no/on/off>: Enable/disable goodbye messages.
- /setwelcome <text>: Set a new welcome message. Supports markdown, buttons, and fillings.
- /resetwelcome: Reset the welcome message.
- /setgoodbye <text>: Set a new goodbye message. Supports markdown, buttons, and fillings.
- /resetgoodbye: Reset the goodbye message.
- /cleanservice <yes/no/on/off>: Delete all service messages. Those are the annoying 'x joined the group' notifications you see when people join.
- /cleanwelcome <yes/no/on/off>: Delete old welcome messages. When a new person joins, or after 5 minutes, the previous message will get deleted.

**Examples:**
- Get the welcome message without any formatting
-> /welcome noformat
"""
wlc_btn = [
    Button.inline("CAPTCHA", data="captcha"),
    Button.inline("Formatting", data="formatting"),
], [Button.inline("Back", data="go_back")]
antiflood = """
**Antiflood**

You know how sometimes, people join, send 100 messages, and ruin your chat? With antiflood, that happens no more!

Antiflood allows you to take action on users that send more than x messages in a row. Actions are: ban/kick/mute/tban/tmute

Admin commands:
- /flood: Get the current antiflood settings
- /setflood <number/off/no>: Set the number of messages after which to take action on a user. Set to '0', 'off', or 'no' to disable.
- /setfloodmode <action type>: Choose which action to take on a user who has been flooding. Options: ban/kick/mute/tban/tmute
"""
blocklist = """
**Blocklists**

Want to stop people asking stupid questions? or ban anyone saying censored words? Blocklists is the module for you!

From blocking rude words, filenames/extensions, to specific emoji, everything is possible.

Admin commands:
- /addblocklist <blocklist trigger> <reason>: Add a blocklist trigger. You can blocklist an entire sentence by putting it in "quotes".
- /rmblocklist <blocklist trigger>: Remove a blocklist trigger.
- /unblocklistall: Remove all blocklist triggers - chat creator only.
- /blocklist: List all blocklisted items.
- /blocklistmode <blocklist mode>: Set the desired action to take when someone says a blocklisted item. Available: nothing/ban/mute/kick/warn/tban/tmute.
- /blocklistdelete <yes/no/on/off>: Set whether blocklisted messages should be deleted. Default: (on)
- /setblocklistreason <reason>: Set the default blocklist reason to warn people with.
- /resetblocklistreason: Reset the default blocklist reason to default - nothing.

Top tip:
Blocklists allow you to use some modifiers to match "unknown" characters. For example, you can use the ? character to match a single occurrence of any non-whitespace character.
You could also use the * modifier, which matches any number of any character. If you want to blocklist urls, this will allow you to match the full thing. It matches every character except spaces. This is cool if you want to block, for example, url shorteners.
"""
locks = """
**Locks**

Do stickers annoy you? or want to avoid people sharing links? or pictures? You're in the right place!

The locks module allows you to lock away some common items in the telegram world; the bot will automatically delete them!

**Admin commands:**
- /lock <item(s)>: Lock one or more items. Now, only admins can use this type!
- /unlock <item(s)>: Unlock one or more items. Everyone can use this type again!
- /locks: List currently locked items.
- /lockwarns <yes/no/on/off>: Enabled or disable whether a user should be warned when using a locked item.
- /locktypes: Show the list of all lockable items.
- /allowlist <url/id/@channelname(s)>: Allowlist a URL, group ID, channel @, or bot @ to stop them being deleted by URL, forward, invitelink, and inline locks. Separate with a space to add multiple items at once. If no arguments are given, returns the current allowlist.
- /rmallowlist <url/id/@channelname(s)>: Remove an item from the allowlist - url, invitelink, and forward locking will now take effect on messages containing it again. Separate with a space to remove multiple items.
- /rmallowlistall: Remove all allowisted items.

**Examples:**
- Lock stickers with:
-> /lock sticker
- You can lock/unlock multiple items by chaining them:
-> /lock sticker photo gif video
- To allow forwards from a specific channel, eg @ElsieSupport, you can allowlist it. You can also use the ID, or invitelink:
-> /allowlist @ElsieSupport
"""
fedz = """
**Federations**

Ah, group management. It's all fun and games, until you start getting spammers in, and you need to ban them. Then you need to start banning more, and more, and it gets painful.
But then you have multiple groups, and you don't want these spammers in any of your groups - how can you deal? Do you have to ban them manually, in all your groups?

No more! With federations, you can make a ban in one chat overlap to all your other chats.
You can even appoint federation admins, so that your trustworthiest admins can ban across all the chats that you want to protect.
"""
admin = """
**Admin**

Make it easy to promote and demote users with the admin module!

**Admin commands:**
- /promote <reply/username/mention/userid>: Promote a user.
- /demote <reply/username/mention/userid>: Demote a user.
- /adminlist: List the admins in the current chat
- /anonadmin <yes/no/on/off>: Allow anonymous admins to use all commands without checking their permissions. Not recommended.
"""
purge = """
**Purges**

Need to delete lots of messages? That's what purges are for!

**Admin commands:**
- /purge: Delete all messages from the replied to message, to the current message.
- /purge <X>: Delete the following X messages after the replied to message.
- /spurge: Same as purge, but doesnt send the final confirmation message.
- /del: Deletes the replied to message.
- /purgefrom: Reply to a message to mark the message as where to purge from - this should be used followed by a /purgeto.
- /purgeto: Delete all messages between the replied to message, and the message marked by the latest /purgefrom.

**Examples:**
- Delete all messages from the replied to message, until now.
-> /purge
- Mark the first message to purge from (as a reply).
-> /purgefrom
- Mark the message to purge to (as a reply). All messages between the previously marked /purgefrom and the newly marked /purgeto will be deleted.
-> /purgeto
"""
pin = """
**Pin**

All the pin related commands can be found here; keep your chat up to date on the latest news with a simple pinned message!

**User commands:**
- /pinned: Get the current pinned message.

**Admin commands:**
- /pin: Pin the message you replied to. Add 'loud' or 'notify' to send a notification to group members.
- /permapin <text>: Pin a custom message through the bot. This message can contain markdown, buttons, and all the other cool features.
- /unpin: Unpin the current pinned message. If used as a reply, unpins the replied to message.
- /unpinall: Unpins all pinned messages.
- /antichannelpin <yes/no/on/off>: Don't let telegram auto-pin linked channels. If no arguments are given, shows current setting.
- /cleanlinked <yes/no/on/off>: Delete messages sent by the linked channel.
"""

approve = """
**Approval**

Sometimes, you might trust a user not to send unwanted content.
Maybe not enough to make them admin, but you might be ok with locks, blacklists, and antiflood not applying to them.

That's what approvals are for - approve of trustworthy users to allow them to send 

**Admin commands:**
- /approval: Check a user's approval status in this chat.

**Admin commands:**
- /approve: Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
- /unapprove: Unapprove of a user. They will now be subject to locks, blacklists, and antiflood again.
- /approved: List all approved users.
- /unapproveall: Unapprove ALL users in a chat. This cannot be undone.
"""
note = """
**Notes**

Save data for future users with notes!

Notes are great to save random tidbits of information; a phone number, a nice gif, a funny picture - anything!

**User commands:**
- /get `<notename>`: Get a note.
- #notename: Same as /get.

**Admin commands:**
- /save `<notename> <note text>`: Save a new note called "word". Replying to a message will save that message. Even works on media!
- /clear `<notename>`: Delete the associated note.
- /notes: List all notes in the current chat.
- /saved: Same as /notes.
- /clearall: Delete ALL notes in a chat. This cannot be undone.
- /privatenotes: Whether or not to send notes in PM. Will send a message with a button which users can click to get the note in PM.
"""
report = """
**Reports**

We're all busy people who don't have time to monitor our groups 24/7. But how do you react if someone in your group is spamming?

Presenting reports; if someone in your group thinks someone needs reporting, they now have an easy way to call all admins.

**User commands:**
- /report: Reply to a message to report it for admins to review.
- admin: Same as /report

**Admin commands:**
- /reports <yes/no/on/off>: Enable/disable user reports.

To report a user, simply reply to his message with @admin or /report; Elsie will then reply with a message stating that admins have been notified. This message tags all the chat admins; same as if they had been @'ed.

Note that the report commands do not work when admins use them; or when used to report an admin. Elsie assumes that admins don't need to report, or be reported!
"""
warn = """
**Warnings**

Keep your members in check with warnings; stop them getting out of control!

If you're looking for automated warnings, go read about the blacklist module.

**Admin commands:**
- /warn `<reason>`: Warn a user.
- /dwarn `<reason>`: Warn a user by reply, and delete their message.
- /swarn `<reason>`: Silently warn a user, and delete your message.
- /warns: See a user's warnings.
- /rmwarn: Remove a user's latest warning.
- /resetwarn: Reset all of a user's warnings to 0.
- /resetallwarns: Delete all the warnings in a chat. All users return to 0 warns.
- /warnings: Get the chat's warning settings.
- /setwarnmode `<ban/kick/mute/tban/tmute>`: Set the chat's warn mode.
- /setwarnlimit `<number>`: Set the number of warnings before users are punished.
- /setwarntime `<time>`: Set how long warnings should last.Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.

**Examples:**
- Warn a user.
-> /warn `@user` For disobeying the rules
"""


@Cbot(pattern="^/help ?(.*)")
async def help(event):
    if not event.is_private:
        if event.pattern_match.group(1):
            module = event.pattern_match.group(1)
        else:
            module = "all"
        buttons = Button.url(
            "Click me for help", "t.me/MissElsie_bot?start=help_{}".format(module)
        )
        await event.reply(string, buttons=buttons)
    else:
        if not event.pattern_match.group(1):
            await paginate_gen(event)
        else:
            plugin_name = (event.pattern_match.group(1)).lower()
            await pl_help(event, plugin_name)


async def pl_help(event, plugin_name):
    if plugin_name == "welcome" or plugin_name == "greetings":
        await event.reply(welcome, buttons=wlc_btn)
    elif plugin_name == "antiflood" or plugin_name == "antispam":
        await event.reply(antiflood, buttons=c_button)
    elif (
        plugin_name == "blocklist"
        or plugin_name == "blacklist"
        or plugin_name == "blocklists"
        or plugin_name == "blacklists"
    ):
        await event.reply(blocklist, buttons=bl_button)
    elif plugin_name == "lock" or plugin_name == "locks":
        await event.reply(locks, buttons=c_button)
    elif plugin_name in ["fed", "feds", "federation", "federations"]:
        await event.reply(fedz, buttons=f_button)
    elif plugin_name in ["admin", "admins"]:
        await event.reply(admin, buttons=c_button)
    elif plugin_name in ["purge", "purges", "del", "delete"]:
        await event.reply(purge, buttons=c_button)
    elif plugin_name in ["pin", "pins"]:
        await event.reply(pin, buttons=c_button)
    elif plugin_name in ["approve", "approval"]:
        await event.reply(approve, buttons=c_button)
    elif plugin_name in ["note", "notes"]:
        await event.reply(note, buttons=n_button)
    elif plugin_name in ["report", "reports", "reporting"]:
        await event.reply(report, button=c_button)
    elif plugin_name in ["warn", "warns", "warnings"]:
        await event.reply(warn, buttons=c_button)
    elif plugin_name in ["captcha", "captchas"]:
        await event.reply(captcha, buttons=c_button)
    else:
        await paginate_gen(event)


@Cbot(pattern="^/start help_(.*)")
async def hh(event):
    plugin_name = (event.pattern_match.group(1)).lower()
    if plugin_name == "welcome" or plugin_name == "greetings":
        await event.reply(welcome, buttons=wlc_btn)
    elif plugin_name == "antiflood" or plugin_name == "antispam":
        await event.reply(antiflood, buttons=c_button)
    elif (
        plugin_name == "blocklist"
        or plugin_name == "blacklist"
        or plugin_name == "blocklists"
        or plugin_name == "blacklists"
    ):
        await event.reply(blocklist, buttons=bl_button)
    elif plugin_name == "lock" or plugin_name == "locks":
        await event.reply(locks, buttons=c_button)
    elif plugin_name in ["fed", "feds", "federation", "federations"]:
        await event.reply(fedz, buttons=f_button)
    elif plugin_name in ["admin", "admins"]:
        await event.reply(admin, buttons=c_button)
    elif plugin_name in ["purge", "purges", "del", "delete"]:
        await event.reply(purge, buttons=c_button)
    elif plugin_name in ["pin", "pins"]:
        await event.reply(pin, buttons=c_button)
    elif plugin_name in ["approve", "approval"]:
        await event.reply(approve, buttons=c_button)
    elif plugin_name in ["note", "notes"]:
        await event.reply(note, buttons=n_button)
    elif plugin_name in ["report", "reports", "reporting"]:
        await event.reply(report, button=c_button)
    elif plugin_name in ["warn", "warns", "warnings"]:
        await event.reply(warn, buttons=c_button)
    elif plugin_name in ["captcha", "captchas"]:
        await event.reply(captcha, buttons=c_button)
    elif plugin_name == "all":
        await paginate_gen(event)


@tbot.on(events.CallbackQuery(pattern="n_eu"))
async def la(event):
    buttons = Button.inline("Back", data="n_go_back")
    await event.edit(example, buttons=buttons)


@tbot.on(events.CallbackQuery(pattern="n_go_back"))
async def la(event):
    await event.edit(note, buttons=n_button)


def get_page(id):
    return pagenumber.find_one({"id": id})


def paginate_help(event, page_number, loaded_plugins, prefix):
    number_of_rows = 15
    number_of_cols = 3

    to_check = get_page(id=event.sender_id)

    if not to_check:
        pagenumber.insert_one({"id": event.sender_id, "page": page_number})

    else:
        pagenumber.update_one(
            {
                "_id": to_check["_id"],
                "id": to_check["id"],
                "page": to_check["page"],
            },
            {"$set": {"page": page_number}},
        )

    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        custom.Button.inline(
            "{}".format(x.replace("_", " ")), data="us_plugin_{}".format(x)
        )
        for x in helpable_plugins
    ]
    pairs = list(
        zip(
            modules[::number_of_cols],
            modules[1::number_of_cols],
            modules[2::number_of_cols],
        )
    )
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    pairs = pairs[modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)] + [
        (custom.Button.inline("Go back", data="m_menu"),)
    ]
    return pairs


async def paginate_gen(event):
    buttons = paginate_help(event, 0, CMD_LIST, "helpme")
    await event.reply(help_str, buttons=buttons)


@tbot.on(events.CallbackQuery(pattern=r"go_back"))
async def go_back(event):
    c = pagenumber.find_one({"id": event.sender_id})
    number = c["page"]
    buttons = paginate_help(event, number, CMD_LIST, "helpme")
    await event.edit(help_str, buttons=buttons)


@tbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"us_plugin_(.*)")))
async def on_plug_in_callback_query_handler(event):
    plugin_name = event.data_match.group(1).decode("UTF-8")
    plugin_name = plugin_name.lower()
    if plugin_name == "greetings":
        await event.edit(welcome, buttons=wlc_btn)
    elif plugin_name == "antiflood":
        await event.edit(antiflood, buttons=c_button)
    elif plugin_name == "blocklists":
        await event.edit(blocklist, buttons=bl_button)
    elif plugin_name == "locks":
        await event.edit(locks, buttons=c_button)
    elif plugin_name == "federations":
        await event.edit(fedz, buttons=f_button)
    elif plugin_name == "admin":
        await event.edit(admin, buttons=c_button)
    elif plugin_name == "purges":
        await event.edit(purge, buttons=c_button)
    elif plugin_name == "pin":
        await event.edit(pin, buttons=c_button)
    elif plugin_name == "approval":
        await event.edit(approve, buttons=c_button)
    elif plugin_name == "notes":
        await event.edit(note, buttons=n_button)
    elif plugin_name == "reports":
        await event.edit(report, button=c_button)
    elif plugin_name == "warnings":
        await event.edit(warn, buttons=c_button)
    elif plugin_name == "captcha":
        await event.edit(captcha, buttons=c_button)
    else:
        await event.edit(
            "seems like, help for this module is not yet implemented!", buttons=c_button
        )


@Cbot(pattern="^/start$")
async def start(event):
    if event.is_group:
        await event.reply("Hi there, I'm online ^_^")
    elif event.is_private:
        start_msg = start_str.format(event.sender.first_name)
        buttons = [
            Button.inline("About", data="about"),
            Button.inline("Help", data="halp"),
        ], [Button.url("Add me to group", "t.me/missElsie_bot?startgroup=true")]
        await event.reply(start_msg, buttons=buttons)


@tbot.on(events.callbackquery.CallbackQuery(pattern="halp"))
async def halp(event):
    buttons = paginate_help(event, 0, CMD_LIST, "helpme")
    await event.edit(help_str, buttons=buttons)


@tbot.on(events.callbackquery.CallbackQuery(pattern="about"))
async def abut(event):
    buttons = (
        [
            Button.inline("T&C", data="tandc"),
            Button.url("Global Logs", "t.me/Elsieglobalbans"),
            Button.inline("About Me", data="a_about"),
        ],
        [
            Button.url("Support Chat", "t.me/Elsiesupport"),
            Button.url("Updates Channel", "t.me/Elsienews"),
        ],
        [Button.inline("Back", data="m_menu")],
    )
    await event.edit(about_str, buttons=buttons)


@tbot.on(events.callbackquery.CallbackQuery(pattern="tandc"))
async def tc(event):
    buttons = Button.inline("Back", data="about")
    await event.edit(tandc, buttons=buttons)


@tbot.on(events.callbackquery.CallbackQuery(pattern="a_about"))
async def abut(event):
    buttons = Button.inline("Back", data="about")
    await event.edit(a_about_str, buttons=buttons)


@tbot.on(events.callbackquery.CallbackQuery(pattern="m_menu"))
async def abut(event):
    start_msg = start_str.format(event.sender.first_name)
    buttons = [
        Button.inline("About", data="about"),
        Button.inline("Help", data="halp"),
    ], [Button.url("Add me to group", "t.me/missElsie_bot?startgroup=true")]
    await event.edit(start_msg, buttons=buttons)
