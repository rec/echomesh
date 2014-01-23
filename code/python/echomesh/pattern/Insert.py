from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.pattern.Maker import maker

@maker('offset', 'length', 'rollover', 'skip')
def insert(color_lists, target=None, offset=None, length=None, rollover=True,
           skip=None):
  assert len(color_lists) == 1
  color_list = color_lists[0]

  skip = int(skip or 1)
  offset = int((offset and offset.evaluate()) or 0)
  if length is None:
    length = Config.get('light', 'count') if target is None else len(target)

  return _insert(color_list, target, offset, length, rollover, skip)

def _insert(color_list, target, offset, length, rollover, skip):
  result = target or ([None] * length)
  for i, light in enumerate(color_list):
    index = offset + i
    if index < 0 or index >= length:
      if rollover:
        index = index % length
      else:
        continue
    result[index] = light

  return result
