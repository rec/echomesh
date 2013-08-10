from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.base import Config
from echomesh.color import ColorTable
from echomesh.util.dict import Setter

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

def evaluate_config():
  config = copy.deepcopy(Config.get_config())
  Setter.apply_function(config, Expression.convert, *UNIT_ADDRESSES)
  Setter.apply_function(config, ColorTable.to_color, *COLOR_ADDRESSES)
  return config
