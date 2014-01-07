from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.pattern.Maker import maker

USE_CECHOMESH = False

@maker('x', 'y', 'reverse_x', 'reverse_y')
def mirror(light_sets, x=None, y=None, reverse_x=False, reverse_y=False):
  assert len(light_sets) == 1
  light_set = light_sets[0]
  if not (x and y):
    default_x, default_y = Config.get('light', 'visualizer', 'layout')
    x = x or default_x
    y = y or default_y

  if USE_CECHOMESH:
    return cechomesh.mirror(
      light_set, int(x), int(y), bool(reverse_x), bool(reverse_y))
  result = [None] * len(light_set)
  for i, light in enumerate(light_set):
    my_x = i % x
    my_y = i // x
    if reverse_x:
      my_x = x - my_x - 1
    if reverse_y:
      my_y = y - my_y - 1
    index = my_x * y + my_y
    if index < len(result):
      result[index] = light

  print('!!!!', result, light_set)
  return result

