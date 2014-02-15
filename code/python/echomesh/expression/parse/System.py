from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random
import time

from echomesh.sound import Level
from echomesh.util.registry.Registry import Registry

class _SystemFunction(object):
  def __init__(self, function_maker, is_constant):
    self.function = None
    self.function_maker = function_maker
    self.is_constant = is_constant

  def prepare(self):
    if not self.function:
      self.function = self.function_maker()

_REGISTRY = Registry('System functions')

def register(name, function, is_constant):
  _REGISTRY.register(_SystemFunction(function, is_constant), name)

register('e', lambda: math.e, True)
register('level', lambda: Level.input_level, False)
register('pi', lambda: math.pi, True)
register('random', lambda: random.random, False)
register('time', lambda: time.time, False)

def get(name):
  result = _REGISTRY.get(name)
  result.prepare()
  return result
