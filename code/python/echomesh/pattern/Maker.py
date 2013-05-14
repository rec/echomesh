from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression.Expression import Expression
from echomesh.pattern import MakerFunctions
from echomesh.util import Call
from echomesh.util import Registry

_REGISTRY = Registry.Registry('pattern types')

def make_pattern(element, desc):
  type_value = desc.pop('type')
  if type_value:
    return desc and _REGISTRY.get(type_value)(element, desc)

def make_patterns(element, description):
  result = {}
  for k, v in description.iteritems():
    result[k] = make_pattern(element, v)
  return result

class Maker(object):
  def __init__(self, element, desc, function, *names):
    self.table = {}
    for k, v in desc.iteritems():
      if k.startswith('pattern'):
        continue
      if k in names:
        v = Expression(v, element)
      self.table[k] = v
    self.function = function
    patterns = desc.get('patterns') or desc.get('pattern')
    if patterns:
      if type(patterns) is not list:
        patterns = [patterns]
      self.patterns = filter(None, (make_pattern(element, p) for p in patterns))
    else:
      self.patterns = []

  def evaluate(self):
    return self()

  def __call__(self):
    table = dict((k, Call.call(v)) for k, v in self.table.iteritems())
    if self.patterns:
      pat = [p() for p in self.patterns]
      return self.function(pat, **table)
    else:
      return self.function(**table)

  def is_constant(self):
    return all(v.is_constant() for v in self.table.itervalues())

def choose(element, desc):
  return Maker(element, desc, MakerFunctions.choose, 'choose')

def concatenate(element, desc):
  return Maker(element, desc, MakerFunctions.concatenate)

def inject(element, desc):
  return Maker(element, desc, MakerFunctions.inject)

def insert(element, desc):
  return Maker(element, desc, MakerFunctions.insert,
               'begin', 'length', 'rollover', 'skip')

def reverse(element, desc):
  return Maker(element, desc, MakerFunctions.reverse)

def spread(element, desc):
  return Maker(element, desc, MakerFunctions.spread, 'colors', 'steps')

def transpose(element, desc):
  return Maker(element, desc, MakerFunctions.transpose,
               'x', 'y', 'reverse_x', 'reverse_y')

_REGISTRY.register(choose)
_REGISTRY.register(concatenate)
_REGISTRY.register(inject)
_REGISTRY.register(insert)
_REGISTRY.register(reverse)
_REGISTRY.register(spread)
_REGISTRY.register(transpose)
