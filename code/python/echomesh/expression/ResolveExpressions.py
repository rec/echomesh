from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.expression import Envelope

UNIT_ADDRESSES = [
  ['light', 'brightness'],
  ['light', 'hardware', 'period'],
  ['light', 'visualizer', 'closes_echomesh'],
]

COLOR_ADDRESSES = [
  ['light', 'visualizer', 'background'],
  ['light', 'visualizer', 'instrument', 'border', 'color'],
  ['light', 'visualizer', 'instrument', 'background'],
]

def resolve_expressions(config, addresses=None):
  config = copy.deepcopy(config)
  addresses = addresses or DEFAULT_ADDRESSES
  for address in addresses:
    cfg = config
    last = len(address) - 1
    for i, part in enumerate(address):
      if i < last:
        cfg = cfg[part]
      else:
        cfg[part] = Expression.convert(cfg[part])
  return config

