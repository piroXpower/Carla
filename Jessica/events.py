import glob
import logging
import sys
import time
from pathlib import Path

from telethon import events

from . import spam, spam_db, tbot


def Cbot(**args):
    pattern = args.get("pattern", None)
    r_pattern = r"^[/?!+]"
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern
    args["pattern"] = pattern.replace("^/", r_pattern, 1)

    def decorator(func):
        async def wrapper(check):
            if check.sender_id:
                if check.sender_id in spam:
                    return
                if not spam_db.get(check.sender_id):
                    spam_db[check.sender_id] = [1, time.time()]
                else:
                    x = spam_db[check.sender_id]
                    if int(time.time() - x[1]) <= 3:
                        if x[0] + 1 >= 4:
                            return spam.append(check.sender_id)
                        else:
                            spam_db[check.sender_id] = [x[0] + 1, time.time()]
                    else:
                        spam_db[check.sender_id] = [1, time.time()]

            try:
                await func(check)
            except BaseException:
                return
            else:
                pass

        tbot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

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
