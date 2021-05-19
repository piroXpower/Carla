import glob
import inspect
import logging
import re
import sys
from pathlib import Path

from telethon import events

from Elsie import CMD_LIST, tbot


def Cbot(**args):
    pattern = args.get("pattern", None)
    r_pattern = r"^[/?!.]"
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern
    args["pattern"] = pattern.replace("^/", r_pattern, 1)
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    reg = re.compile("(.*)")

    if pattern is not None:
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except BaseException:
                pass

            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    def decorator(func):
        tbot.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator


def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib

        import Elsie.events  # pylint:disable=E0602

        path = Path(f"Elsie/modules/{shortname}.py")
        name = "Elsie.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Successfully imported " + shortname)
    else:
        import importlib

        import Elsie.events  # pylint:disable=E0602

        path = Path(f"Elsie/modules/{shortname}.py")
        name = "Elsie.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.Cbot = Cbot
        mod.tbot = tbot
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        sys.modules["Elsie.modules." + shortname] = mod
        print("Successfully imported " + shortname)


path = "Elsie/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))
