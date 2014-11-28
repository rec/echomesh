from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os.path

from echomesh.base import EmptyProject
from echomesh.base import MakeDirs
from echomesh.base import Name

_CREATE_MISSING_DIRECTORY_PROJECT = """

There doesn't seem to be an echomesh project in your directory %s.
Would you like an empty project created for you? (Y/n) """

_PROGRESS_MESSAGE = """
Creating files..."""

_MISSING_DIRECTORY_ERROR = """
No echomesh project found in directory %s.  echomesh must exit.
"""

_CLOSING_MESSAGE = """
Empty echomesh project created.

"""

_PATH_FORMAT = '  %s'

def _print_path(p):
    print(_PATH_FORMAT % p)

def _make_empty_project(path):
    """Make an empty echomesh project at this path."""
    ep = copy.deepcopy(EmptyProject.EMPTY_PROJECT)
    name_text = _NAME % Name.NAME
    ep['data']['name'][Name.NAME] = {'settings.yml': name_text, 'score': None}
    _make(path, ep)
    print(_CLOSING_MESSAGE)

def _make(path, value):
    path = os.path.expanduser(path)
    exists = os.path.exists(path)
    is_dict = isinstance(value, dict)
    if value is None or is_dict:
        if not exists:
            MakeDirs.makedirs(path)
            _print_path(path)
        if is_dict:
            for k, v in value.items():
                _make(os.path.join(path, k), v)
    elif exists:
        print('Not overwriting existing', path)
    else:
        with open(path, 'w') as f:
            f.write(value)
        _print_path(path)

def ask_to_make_empty_project(path):
    yn = '?'
    while yn and yn[0] not in 'yn':
        print(_CREATE_MISSING_DIRECTORY_PROJECT % path, end='')
        yn = raw_input().strip().lower()
    if not (yn and yn[0] == 'n'):
        print(_PROGRESS_MESSAGE)
        _make_empty_project(path)
        return True
    else:
        print(_MISSING_DIRECTORY_ERROR % path)
        return False
