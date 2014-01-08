from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.pattern.Maker import maker

@maker('x', 'y', 'reverse_x', 'reverse_y')
def mirror(light_sets, x=None, y=None, reverse_x=False, reverse_y=False):
  assert len(light_sets) == 1
  if not (x and y):
    default_x, default_y = Config.get('light', 'visualizer', 'layout')
    x = x or default_x
    y = y or default_y

  return cechomesh.mirror_color_list(
    light_sets[0], int(x), int(y), bool(reverse_x), bool(reverse_y))

