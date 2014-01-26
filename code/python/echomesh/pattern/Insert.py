from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.pattern.Pattern import Pattern

class Insert(Pattern):
  PATTERN_COUNT = 1
  OPTIONAL_VARIABLES = 'length', 'offset', 'rollover', 'skip'

  def _evaluate(self):
    color_list = self.patterns()[0]
    skip = int(self.get('skip') or 1)
    offset = int(self.get('offset') or 0)
    length = self.get('length')
    if length is None:
      length = Config.get('light', 'count')
    rollover = bool(self.get('rollover'))

    return cechomesh.insert_color_list(color_list, offset, length, rollover, skip)

