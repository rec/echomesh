from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from cechomesh import to_color
from echomesh.base import Config
from echomesh.expression import Expression
from echomesh.util.dict import Setter

# TODO: this is not used.  Delete it?

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
  Setter.apply_apply_list(config, Expression.convert, *UNIT_ADDRESSES)
  Setter.apply_list(config, to_color, *COLOR_ADDRESSES)
  return config
