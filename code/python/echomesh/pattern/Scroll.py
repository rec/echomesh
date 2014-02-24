from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.pattern.Pattern import Pattern

class Scroll(Pattern):
  OPTIONAL_CONSTANTS = {'x_size': None, 'wrap': False, 'smooth': True}
  OPTIONAL_VARIABLES = {'dx': 0, 'dy': 0}
  PATTERN_COUNT = 1

  def _evaluate(self):
    color_list = self.patterns()[0]

    x_size = self.get('x_size') or Config.get(
      'light', 'visualizer', 'layout')[0]

    return cechomesh.scroll_color_list(
      color_list, self.get('dx'), self.get('dy'), x_size,
      wrap=self.get('wrap'), smooth=self.get('smooth'))
