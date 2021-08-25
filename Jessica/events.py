import glob
import inspect
import logging
import re
import sys
import time
from pathlib import Path

from telethon import events

from Jessica import tbot

spam_db = {}
spam = []


def Cbot(**args):
    pattern = args.get("pattern", None)
    r_pattern = r"^[/?!+]"
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern
    args["pattern"] = pattern.replace("^/", r_pattern, 1)
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    re.compile("(.*)")

    def decorator(func):
        async def wrapper(e):
            if e.sender_id:
                if e.sender_id in spam:
                    return
                if not spam_db.get(e.sender_id):
                    spam_db[e.sender_id] = [1, time.time()]
                else:
                    x = spam_db[e.sender_id]
                    if int(time.time() - x[1]) <= 3:
                        if x[0] + 1 >= 4:
                            return spam.append(e.sender_id)
                        else:
                            spam_db[e.sender_id] = [x[0] + 1, time.time()]
            await wrapper(e)

        tbot.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator


def Cquery(**args):
    pattern = args.get("pattern", None)

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    def decorator(func):
        tbot.add_event_handler(func, events.InlineQuery(**args))
        return func

    return decorator


def Cinline(**args):
    def decorator(func):
        tbot.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator


def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib

        import Jessica.events  # pylint:disable=E0602

        path = Path(f"Jessica/modules/{shortname}.py")
        name = "Jessica.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Successfully imported " + shortname)
    else:
        import importlib

        import Jessica.events  # pylint:disable=E0602

        path = Path(f"Jessica/modules/{shortname}.py")
        name = "Jessica.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.Cbot = Cbot
        mod.tbot = tbot
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        sys.modules["Jessica.modules." + shortname] = mod
        print("Successfully imported " + shortname)


path = "Jessica/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))
