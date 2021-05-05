import inspect, time, logging, re, glob, asyncio, sys
from pathlib import Path
from telethon import events, Button
from telethon.tl import functions, types
from Carla import CMD_LIST, LOAD_PLUG, tbot

def Cbot(**args):
    pattern = args.get('pattern', None)
    r_pattern = r'^[/?!.]'
    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern
    args['pattern'] = pattern.replace('^/', r_pattern, 1)

    def decorator(func):
        tbot.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator

def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import Carla.events

        path = Path(f"Carla/modules/{shortname}.py")
        name = "Carla.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Successfully imported " + shortname)
    else:
        import importlib
        import Carla.events

        path = Path(f"Carla/modules/{shortname}.py")
        name = "Carla.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.Cbot = Cbot
        mod.tbot = tbot
        mod.logger = logging.getLogger(shortname)
        spec.loader.exec_module(mod)
        sys.modules["Carla.modules." + shortname] = mod
        print("Successfully imported " + shortname)

path = "Carla/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))
