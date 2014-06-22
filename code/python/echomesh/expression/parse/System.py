from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random
import time

from echomesh.util.registry.Registry import Registry

class _SystemFunction(object):
  def __init__(self, function_maker, is_constant, needs_element):
    self.function = None
    self.function_maker = function_maker
    self.is_constant = is_constant
    self.needs_element = needs_element

  def prepare(self):
    if not self.function:
      self.function = self.function_maker()

  def evaluate(self, element):
    return self.function(element) if self.needs_element else self.function

_REGISTRY = Registry('System functions')

def register(name, function, is_constant, needs_element=False):
  _REGISTRY.register(
    _SystemFunction(function, is_constant, needs_element), name)

def _elapsed(element):
  return element.elapsed_time()

def _level():
  from echomesh.sound import Level
  return Level.input_level()

register('e', lambda: math.e, True)
register('elapsed', lambda: _elapsed, False, needs_element=True)
register('level', lambda: _level, False)
register('pi', lambda: math.pi, True)
register('random', lambda: random.random, False)
register('time', lambda: time.time, False)

def get(name):
  result = _REGISTRY.get(name)
  result.prepare()
  return result
