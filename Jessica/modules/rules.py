import Jessica.modules.mongodb.rules_db as db
from Jessica.events import Cbot, Cinline
from telethon import Button
from . import can_change_info

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
    elif args in pos:
        await event.reply("Use of /rules will send the rules to the user's PM.")
        db.set_private_rules(event.chat_id, True)
    elif args in neg:
        await event.reply(
            f"All /rules commands will send the rules to {event.chat.title}."
        )
        db.set_private_rules(event.chat_id, False)
    else:
        await event.reply("I only understand the following: yes/no/on/off")


@Cbot(pattern="^/setrules ?(.*)")
async def set_r(event):
    if (
        event.text.startswith(".setrulesbutton")
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


async def a_rules(event, mode):
    global anon_db
    anon_db[event.id] = event.text
    cb_data = str(event.id) + "|" + str(mode)
    a_buttons = Button.inline("Click to prove admin", data="ranon_{}".format(cb_data))
    await event.reply(
        "It looks like you're anonymous. Tap this button to confirm your identity.",
        buttons=a_buttons,
    )


@Cinline(pattern=r"ranon(\_(.*))")
async def rules_anon(e):
    d_ata = ((event.pattern_match.group(1)).decode()).split("_", 1)[1]
    da_ta = d_ata.split("|", 1)
    event_id = int(da_ta[0])
    mode = da_ta[1]
    await event.answer(str(event_id) + "|" + mode, alert=True)
