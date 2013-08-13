from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random
import time

from echomesh.sound import Level
from echomesh.util.registry.Registry import Registry

class _SystemFunction(object):
  def __init__(self, function, is_constant):
    self.function = function
    self.is_constant = is_constant

_REGISTRY = Registry('System functions')

def register(name, function, is_constant):
  _REGISTRY.register(_SystemFunction(function, is_constant), name)

register('e', math.e, True)
register('level', Level.input_level, False)
register('pi', math.pi, True)
register('random', random.random, False)
register('time', time.time, False)

get = _REGISTRY.get
