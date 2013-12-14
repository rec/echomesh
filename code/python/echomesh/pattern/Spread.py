from __future__ import absolute_import, division, print_function, unicode_literals

import math
import six

from echomesh.color import ColorSpread
from echomesh.base import Config
from echomesh.pattern.Maker import maker

def _to_list(s):
  if s is None:
    return []
  if isinstance(s, six.string_types):
    return [i.strip() for i in s.split(', ')]
  elif not isinstance(s, (list, tuple)):
    return [s]
  else:
    return s

@maker('steps')
def spread(colors=None, steps=None, transforms=None):
  assert colors

  colors = _to_list(colors)
  transforms = _to_list(transforms)

  if len(colors) == 1:
    colors = [colors[0], colors[0]]

  if steps is None:
    steps = [math.ceil(Config.get('light', 'count') / len(colors))]
  else:
    steps = _to_list(steps.evaluate())

  result = []
  for i in xrange(len(colors) - 1):
    s = steps[i if i < len(steps) else -1]
    t = transforms and transforms[i if i < len(transforms) else -1]
    result.extend(ColorSpread.color_name_spread(begin=colors[i],
                                                end=colors[i + 1],
                                                steps=s,
                                                transform=t))
  return result

