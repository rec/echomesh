from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.color.LightCount import light_count
from echomesh.pattern.Pattern import Pattern

class Insert(Pattern):
  PATTERN_COUNT = 1
  SETTINGS = {
    'length': {'default': 0},
    'offset': {'default': 0},
    'rollover': {'default': False},
    'skip': {'default': 1},
    }

  def _evaluate(self):
    color_lists = self.patterns()
    assert len(color_lists) == 1
    color_list = color_lists[0]

    skip = int(self.get('skip'))
    offset = int(self.get('offset'))
    length = self.get('length')
    if not length:
      length = light_count(Config.get)
    rollover = bool(self.get('rollover'))

    return cechomesh.insert_color_list(color_list, offset, length, rollover, skip)

