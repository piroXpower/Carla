from Carla import tbot
from Carla.events import Cbot
from telethon import Button
import re
from typing import List

BTN_URL_REGEX = re.compile(
    r"(\[([^\[]+?)\]\((buttonurl|buttonalert):(?:/{0,2})(.+?)(:same)?\))"
)

SMART_OPEN = "“"
SMART_CLOSE = "”"
START_CHAR = ("'", '"', SMART_OPEN)

def split_quotes(text: str) -> List:
    if any(text.startswith(char) for char in START_CHAR):
        counter = 1  # ignore first char -> is some kind of quote
        while counter < len(text):
            if text[counter] == "\\":
                counter += 1
            elif text[counter] == text[0] or (
                text[0] == SMART_OPEN and text[counter] == SMART_CLOSE
            ):
                break
            counter += 1
        else:
            return text.split(None, 1)

        # 1 to avoid starting quote, and counter is exclusive so avoids ending
        key = remove_escapes(text[1:counter].strip())
        # index will be in range, or `else` would have been executed and returned
        rest = text[counter + 1 :].strip()
        if not key:
            key = text[0] + text[0]
        return list(filter(None, [key, rest]))
    else:
        return text.split(None, 1)

def parser(text, keyword):
    if "buttonalert" in text:
        text = text.replace("\n", "\\n").replace("\t", "\\t")
    buttons = []
    note_data = ""
    prev = 0
    i = 0
    alerts = []
    for match in BTN_URL_REGEX.finditer(text):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            note_data += text[prev : match.start(1)]
            prev = match.end(1)
            if match.group(3) == "buttonalert":
                # create a thruple with button label, url, and newline status
                if bool(match.group(5)) and buttons:
                    buttons[-1].append(
                        Button.inline(
                            match.group(2),
                            data=f"alertmessage:{i}:{keyword}",
                        )
                    )
                else:
                    buttons.append(
                        [
                            Button.inline(
                                match.group(2),
                                data=f"alertmessage:{i}:{keyword}",
                            )
                        ]
                    )
                i = i + 1
                alerts.append(match.group(4))
            else:
                if bool(match.group(5)) and buttons:
                    buttons[-1].append(
                        Button.url(
                            match.group(2), match.group(4).replace(" ", "")
                        )
                    )
                else:
                    buttons.append(
                        [
                            Button.url(
                                match.group(2), match.group(4).replace(" ", "")
                            )
                        ]
                    )

        # if odd, escaped -> move along
        else:
            note_data += text[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += text[prev:]

    try:
        return note_data, buttons, alerts
    except:
        return note_data, buttons, None
BUTTONS = {}


def get_reply_msg_btns_text(message):
    text = ""
    for column in message.reply_markup.rows:
        btn_num = 0
        for btn in column.buttons:
            btn_num += 1
            name = btn.text

            if btn.url:
                url = btn.url
                text += f"\n[{btn.text}](btnurl:{btn.url}*!repl!*)"
            elif btn.data:
                text += parse_button(btn.data, name)
            if btn_num > 1:
                text = text.replace("*!repl!*", ":same")
            else:
                text = text.replace("*!repl!*", "")
    return text

def parse_button(data, name):
    raw_button = data.split("_")
    raw_btn_type = raw_button[0]

    pattern = re.match(r"btn(.+)(sm|cb|start)", raw_btn_type)
    if not pattern:
        return ""

    action = pattern.group(1)
    args = raw_button[1]

    if action in BUTTONS:
        text = f"\n[{name}](btn{action}:{args}*!repl!*)"
    else:
        if args:
            text = f"\n[{name}].(btn{action}:{args})"
        else:
            text = f"\n[{name}].(btn{action})"

    return text

@Cbot(pattern="^/btn ?(.*)")
async def tt(event):
 text = event.pattern_match.group(1)
 try:
  brb = get_reply_msg_btns_text(await event.get_reply_message())
 except Exception as e:
  return await event.respond(str(e))
 await event.respond(str(brb))

def remove_escapes(text: str) -> str:
    counter = 0
    res = ""
    is_escaped = False
    while counter < len(text):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
        counter += 1
    return res


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + "B"
