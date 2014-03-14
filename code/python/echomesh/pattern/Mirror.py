from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.pattern.Pattern import Pattern

class Mirror(Pattern):
  OPTIONAL_CONSTANTS = {
    'x': {
      'default': 0,
      'constant': True,
      'help': '',
      },
    'y': {
      'default': 0,
      'constant': True,
      'help': '',
      },
    'reverse_x': {
      'default': False,
      'constant': True,
      'help': '',
      },
    'reverse_y': {
      'default': False,
      'constant': True,
      'help': '',
      },
    }
  PATTERN_COUNT = 1

  def _evaluate(self):
    color_lists = self.patterns()
    assert len(color_lists) == 1
    color_list = color_lists[0]

    x = self.get('x')
    y = self.get('y')
    if not (x and y):
      default_x, default_y = Config.get('light', 'visualizer', 'layout')
      x = x or default_x
      y = y or default_y

    return cechomesh.mirror_color_list(
      color_list, int(x), int(y),
      bool(self.get('reverse_x')), bool(self.get('reverse_y')))

