import os
from importlib import import_module
from inspect import isclass
from os.path import abspath, join, dirname, basename

from app import BaseFlaskView

PROJ_DIR = abspath(join(dirname(abspath(__file__))))
APP_MODULE = basename(PROJ_DIR)


def get_modules(module):
    """Returns all .py modules in given file_dir that are not __init__."""
    file_dir = abspath(join(PROJ_DIR, module))
    for root, dirnames, files in os.walk(file_dir):
        mod_path = '{}{}'.format(APP_MODULE, root.split(PROJ_DIR)[1]).replace('/', '.')
        for filename in files:
            if filename.endswith('.py') and not filename.startswith('__init__'):
                yield '.'.join([mod_path, filename[0:-3]])


def dynamic_loader(module, compare):
    """Iterates over all .py files in `module` directory, finding all classes that
    match `compare` function.
    Other classes/objects in the module directory will be ignored.

    Returns unique items found.
    """
    items = []
    for mod in get_modules(module):
        module = import_module(mod)
        if module.__name__.endswith(".routes"):
            objs = [cls for name, cls in module.__dict__.items() if isinstance(cls, type)]
            items += [o for o in objs if compare(o) and o not in items]
    return items


def get_views():
    """Dynamic view finder."""
    return dynamic_loader('', is_view)


def is_view(item):
    """Determine if `item` is a `FlaskView` subclass
    (because we don't want to register `FlaskView` itself).
    """
    return item is not BaseFlaskView and isclass(item) and issubclass(item, BaseFlaskView)  # and not item.__ignore__()
