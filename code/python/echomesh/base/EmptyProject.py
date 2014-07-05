from __future__ import absolute_import, division, print_function, unicode_literals

_SETTINGS = """\
# This is your master settings file.
# Put your settings here.
"""

_README = """\
This is an empty echomesh directory.

Put your sound or image files in asset/image or asset/audio.
Put your settings in data/master/settings.yml
"""

_NAME = """\
# This is where you store settings and scores that are only
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

  'data': {
    'master': {
      'settings': { 'settings.yml':  _SETTINGS, },
      'output': None,
      'pattern': None,
      'scene': None,
      'score': { 'sample-score.yml': _SCORE, },
    },

    'name': {}
  },

  'log': None,

  'README.txt': _README,
}
