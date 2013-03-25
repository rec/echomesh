from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import MakeDirs
from echomesh.base import Name

import copy
import os.path

_CLOSING_MESSAGE = """
Empty echomesh project created.

"""

def make_empty_project(path):
  """Make an empty echomesh project at this path."""
  print()
  ep = copy.deepcopy(EMPTY_PROJECT)
  name_text = _NAME % Name.NAME
  ep['command']['name'][Name.NAME] = {'config.yml': name_text, 'score': None}
  _make(path, ep)
  print(_CLOSING_MESSAGE)

def _make(path, value):
  path = os.path.expanduser(path)
  exists = os.path.exists(path)
  is_dict = isinstance(value, dict)
  if value is None or is_dict:
    if not exists:
      MakeDirs.makedirs(path)
      print(path)
    if is_dict:
      for k, v in value.iteritems():
        _make(os.path.join(path, k), v)
  elif exists:
    print('Not overwriting existing', path)
  else:
    with open(path, 'w') as f:
      f.write(value)
    print(path)

_CONFIG = """\
# This is your master config file.
# Put your configuration settings here.
"""

_README = """\
This is an empty echomesh directory.

Put your sound or image files in asset/image or asset/audio.
Put your configurations in command/master/config.yml
"""

_NAME = """\
# This is where you store configurations and scores that are only
# used on this specific machine, %s.
"""

_SCORE = """\
# This is a sample score.

type: print
text: Hello, world!

"""

EMPTY_PROJECT = {
  'asset': {
    'audio': None,
    'image': None,
  },

  'cache': None,

  'command': {
    'master': {
      'config.yml':  _CONFIG,
      'score': {
        'score.yml': _SCORE,
      },
    },

    'name': {}
  },

  'log': None,

  'README.txt': _README,
}
