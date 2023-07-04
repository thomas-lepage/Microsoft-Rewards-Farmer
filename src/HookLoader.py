
from __future__ import print_function

import sys
import os
from collections import namedtuple
import importlib
import importlib.util
import glob

from pathlib import Path

Hooks = namedtuple('Hooks', 'account_completed account_error')
_HOOKS = Hooks._fields

def hook(f):
    fname = f.__name__
    if fname not in _HOOKS:
        msg = '{0} is not a valid hook. Possible hooks are: {1}'.format(fname, _HOOKS)
        raise ImportError(msg)
    return f

paths = ['.', 'inner']

def select_hooks(module):
    for _hook in _HOOKS:
        loaded_hook = getattr(module, _hook, None)
        if loaded_hook:
            yield _hook, loaded_hook

def load_hooks(paths):
    for path in paths:
        if Path(path).exists():
            try:
                for file in os.listdir(os.path.dirname(__file__) + '/hooks'):
                    if os.path.isfile(os.path.dirname(__file__) + '/hooks/' + file):
                        spec = importlib.util.find_spec('hooks.' + Path(file).stem, '.')
                        module = spec.loader.load_module()
                        for hooktuple in select_hooks(module):
                            yield hooktuple # this would be a 'yield from' in Python3 only
                        del module
            except ImportError as err:
                print(err, file=sys.stderr)

def discover_hooks(paths):
    hooks = {h:[] for h in _HOOKS}
    for hookname, hook in load_hooks(paths):
        hooks[hookname].append(hook)


    return Hooks(**hooks)