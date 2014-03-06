from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.color.LightCount import light_count
from echomesh.pattern.Pattern import Pattern

class Insert(Pattern):
  PATTERN_COUNT = 1
  OPTIONAL_VARIABLES = {
    'length': None, 'offset': 0, 'rollover': False, 'skip': 1}

  def _evaluate(self):
    color_lists = self.patterns()
    assert len(color_lists) == 1
    color_list = color_lists[0]

    skip = int(self.get('skip') or 1)
    offset = int(self.get('offset') or 0)
    length = self.get('length')
    if length is None:
      length = light_count(Config.get)
    rollover = bool(self.get('rollover'))

    return cechomesh.insert_color_list(color_list, offset, length, rollover, skip)

