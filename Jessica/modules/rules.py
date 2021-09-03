from telethon import Button

import neko.modules.mongodb.rules_db as db
from neko import CMD_HELP
from neko.events import Cbot, Cinline

from . import button_parser, can_change_info, cb_can_change_info

anon_db = {}


@Cbot(pattern="^/privaterules ?(.*)")
async def pr(event):
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await a_rules(event, "privaterules")
    if event.is_group:
        if not await can_change_info(event, event.sender_id):
            return
    args = event.pattern_match.group(1)
    rules = db.get_rules(event.chat_id)
    if not rules:
        return await event.reply(
            "You haven't set any rules yet; how about you do that first?"
        )
    if not args:
        mode = db.get_private_rules(event.chat_id)
        if mode:
            await event.reply("Use of /rules will send the rules to the user's PM.")
        else:
            await event.reply(
                f"All /rules commands will send the rules to {event.chat.title}."
            )
    elif args in ["on", "yes", "y"]:
        await event.reply("Use of /rules will send the rules to the user's PM.")
        db.set_private_rules(event.chat_id, True)
    elif args in ["off", "no", "n"]:
        await event.reply(
            f"All /rules commands will send the rules to {event.chat.title}."
        )
        db.set_private_rules(event.chat_id, False)
    else:
        await event.reply("I only understand the following: yes/no/on/off")


@Cbot(pattern="^/setrules ?(.*)")
async def set_r(event):
    if (
        event.text.startswith("+setrulesbutton")
        or event.text.startswith("?setrulesbutton")
        or event.text.startswith("!setrulesbutton")
        or event.text.startswith("/setrulesbutton")
    ):
        return
    if event.is_private:
        return await event.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not event.from_id:
        return await a_rules(event, "setrules")
    if event.is_group and event.from_id:
        if not await can_change_info(event, event.sender_id):
            return
    if not event.reply_to and not event.pattern_match.group(1):
        return await event.reply("You need to give me rules to set!")
    elif event.reply_to:
        r_text = ""
        r_msg = await event.get_reply_message()
        if r_msg.text:
            r_text = r_msg.text
        if r_msg.reply_markup:
            buttons = get_reply_msg_btns_text(r_msg)
            r_text = r_text + str(buttons)
        if r_msg.media and not r_msg.text:
            return await event.reply("You need to give me rules to set!")
    elif event.pattern_match.group(1):
        r_text = event.text.split(None, 1)[1]
    await event.reply("New rules for {} set successfully!".format(event.chat.title))
    db.set_rules(event.chat_id, r_text)


@Cbot(pattern="^/resetrules")
async def reset_rules(e):
    if (
        e.text.startswith("+resetrulesbutton")
        or e.text.startswith("/resetrulesbutton")
        or e.text.startswith("?resetrulesbutton")
        or e.text.startswith("!resetrulesbutton")
    ):
        return
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await a_rules(e, "resetrules")
    if e.is_group:
        if not await can_change_info(e, e.sender_id):
            return
    await e.reply(f"Rules for {e.chat.title} were successfully cleared!")
    db.del_rules(e.chat_id)


r_btn = """
The rules button will be called:
`{}`

To change the button name, try this command again followed by the new name
"""


@Cbot(pattern="^/setrulesbutton ?(.*)")
async def set_rules_button(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await a_rules(e, "setrulesbutton")
    rg = e.pattern_match.group(1)
    if not rg:
        x = db.get_rules_button(e.chat_id)
        await e.reply(r_btn.format(x))
    elif len(rg) > 100:
        r_over = "Your new rules button name is too long; please make it shorter (under 100 characters)."
        await e.reply(r_over)
    elif rg:
        r_g = e.text.split(None, 1)[1]
        db.set_rules_button(e.chat_id, r_g)
        await e.reply("Updated the rules button name!")


@Cbot(pattern="^/resetrulesbutton")
async def p(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    if not e.from_id:
        return await a_rules(e, "resetrulesbutton")
    if e.is_group:
        if not await can_change_info(e, e.sender_id):
            return
    await e.reply("Reset the rules button name to default")
    db.set_rules_button(e.chat_id, "Rules")


@Cbot(pattern="^/(rules|rule|Rules)")
async def rules(e):
    if e.is_private:
        return await e.reply(
            "This command is made to be used in group chats, not in pm!"
        )
    rules = db.get_rules(e.chat_id)
    pr = db.get_private_rules(e.chat_id)
    if not rules:
        return await e.reply(
            "The group admins haven't set any rules for this chat yet. This probably doesn't mean it's lawless though...!"
        )
    elif pr:
        button_name = db.get_rules_button(e.chat_id)
        str(e.chat_id)
        x = Button.url(
            button_name, "t.me/MissNeko_Bot?start=_rules_{}".format(e.chat_id)
        )
        await e.reply("Click on the button to see the chat rules!", buttons=x)
    elif not pr:
        x_rules, buttons = button_parser(rules)
        await e.reply(f"The Rules for {e.chat.title} are:\n" + x_rules, buttons=buttons)


@Cbot(pattern="^/start _rules(.*)")
async def private_r_trigger(e):
    if not e.is_private:
        return
    chat_id = int((e.pattern_match.group(1)).split("_", 1)[1])
    rules = (
        db.get_rules(chat_id)
        or "The group admins haven't set any rules for this chat yet. This probably doesn't mean it's lawless though...!"
    )
    await e.reply("Rules are:\n" + rules)


async def a_rules(event, mode):
    global anon_db
    if event.reply_to:
        anon_db[event.id] = (await event.get_reply_message()).text or "None"
    else:
        try:
            anon_db[event.id] = event.text.split(None, 1)[1]
        except IndexError:
            anon_db[event.id] = "None"
    cb_data = str(event.id) + "|" + str(mode)
    a_buttons = Button.inline("Click to prove admin", data="ranon_{}".format(cb_data))
    await event.reply(
        "It looks like you're anonymous. Tap this button to confirm your identity.",
        buttons=a_buttons,
    )


@Cinline(pattern=r"ranon(\_(.*))")
async def rules_anon(e):
    d_ata = ((e.pattern_match.group(1)).decode()).split("_", 1)[1]
    da_ta = d_ata.split("|", 1)
    event_id = int(da_ta[0])
    mode = da_ta[1]
    if not await cb_can_change_info(e, e.sender_id):
        return
    try:
        cb_data = anon_db[event_id]
    except KeyError:
        return await e.edit("This requests has been expired.")
    if mode == "setrules":
        if cb_data == "None":
            await e.edit("You need to give me rules to set!")
        else:
            await e.edit("New rules for {} set successfully!".format(e.chat.title))
            db.set_rules(e.chat_id, cb_data)
    elif mode == "privaterules":
        rules = db.get_rules(e.chat_id)
        if not rules and cb_data != "None":
            return await e.edit(
                "You haven't set any rules yet; how about you do that first?"
            )
        elif cb_data == "None":
            mode = db.get_private_rules(e.chat_id)
            if mode:
                await e.edit("Use of /rules will send the rules to the user's PM.")
            else:
                await e.edit(
                    f"All /rules commands will send the rules to {e.chat.title}."
                )
        elif cb_data in ["on", "yes"]:
            await e.edit("Use of /rules will send the rules to the user's PM.")
            db.set_private_rules(e.chat_id, True)
        elif cb_data in ["off", "no"]:
            await e.edit(f"All /rules commands will send the rules to {e.chat.title}.")
            db.set_private_rules(e.chat_id, False)
        else:
            await e.edit("I only understand the following: yes/no/on/off")
    elif mode == "resetrules":
        await e.reply(f"Rules for {event.chat.title} were successfully cleared!")
        db.del_rules(event.chat_id)
    elif mode == "setrulesbutton":
        if not cb_data:
            x = db.get_rules_button(e.chat_id)
            await e.edit(r_btn.format(x))
        elif len(rg) > 100:
            r_over = "Your new rules button name is too long; please make it shorter (under 100 characters)."
            await e.edit(r_over)
        elif rg:
            r_g = e.text.split(None, 1)[1]
            db.set_rules_button(e.chat_id, r_g)
            await e.edit("Updated the rules button name!")
    elif mode == "resetrulesbutton":
        await e.edit("Reset the rules button name to default")
        db.set_rules_button(e.chat_id, "Rules")


__name__ = "rules"
__help__ = """
Every chat works with different rules; this module will help make those rules clearer!

**User commands:**
- /rules: Check the current chat rules.

**Admin commands:**
- /setrules <text>: Set the rules for this chat. Supports markdown, buttons, fillings, etc.
- /privaterules <yes/no/on/off>: Enable/disable whether the rules should be sent in private.
- /resetrules: Reset the chat rules to default.
- /setrulesbutton: Set the rules button name when using {rules}.
- /resetrulesbutton: Reset the rules button name from {rules} to default.
"""
CMD_HELP.update({__name__: [__name__, __help__]})
