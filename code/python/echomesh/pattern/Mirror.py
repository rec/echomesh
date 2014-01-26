from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.pattern.Pattern import Pattern

class Mirror(
  OPTIONAL_CONSTANTS = 'x', 'y', 'reverse_x', 'reverse_y'
  PATTERN_COUNT = 1

  def _evaluate(self, x=None, y=None, reverse_x=False, reverse_y=False):
    assert len(light_sets) == 1
    x = self.get('x')
    y = self.get('y')
    if not (x and y):
      default_x, default_y = Config.get('light', 'visualizer', 'layout')
      x = x or default_x
      y = y or default_y

    return cechomesh.mirror_color_list(
      self.patterns()[0], int(x), int(y),
      bool(self.get('reverse_x')), bool(self.get('reverse_y')))

