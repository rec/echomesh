from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.pattern.Maker import maker

USE_CECHOMESH = True

@maker('offset', 'length', 'rollover', 'skip')
def insert(color_lists, offset=None, length=None, rollover=True, skip=None):
  assert len(color_lists) == 1
  color_list = color_lists[0]

  skip = int((skip and skip.evaluate()) or 1)
  offset = int((offset and offset.evaluate()) or 0)
  if length is None:
    length = Config.get('light', 'count')

  return cechomesh.insert_color_list(color_list, offset, length, rollover, skip)
