from Jessica import BOT_ID, ubot


@tbot.on(events.NewMessage())
async def cb(e):
    if e.media or e.fwd_from:
        return
    if e.reply_to:
        r_e = await e.get_reply_message()
        if r_e.sender_id == BOT_ID:
            pass
        else:
            return
    else:
        return
    q = e.text
    async with ubot.conversation("@KukiAI_bot") as chat:
        await chat.send_message(str(q))
        res = await chat.get_response()
        if res.text:
            await e.reply(res.text)
        elif res.media:
            re_re = await ubot.send_message("@MissNeko_Bot", file=res.media)
            await e.reply(file=re_re.media)
            await re_re.delete()
