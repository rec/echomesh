from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorSpread
from echomesh.color import Combiner
from echomesh.expression.Expression import Expression
from echomesh.util import Call
from echomesh.util import Registry

_REGISTRY = Registry.Registry('pattern types')

def make_pattern(element, desc):
  return desc and _REGISTRY.get(desc.pop('type'))(element, desc)

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
    if type(patterns) is not list:
      patterns = [patterns]
    self.patterns = filter(None, (make_pattern(element, p) for p in patterns))

  def evaluate(self):
    return self()

  def __call__(self):
    table = dict((k, Call.call(v)) for k, v in self.table.iteritems())
    if self.patterns:
      pat = [p() for p in self.patterns]
      if len(pat) == 1:
        pat = pat[0]
      return self.function(pat, **table)
    else:
      return self.function(**table)

  def is_constant(self):
    return all(v.is_constant() for v in self.table.itervalues())

def inject(element, desc):
  return Maker(element, desc, Combiner.inject)

def insert(element, desc):
  return Maker(element, desc, Combiner.insert,
               'begin', 'length', 'rollover', 'skip')

def reverse(element, desc):
  return Maker(element, desc, reversed)

def spread(element, desc):
  return Maker(element, desc, ColorSpread.color_name_spread, 'steps')

def choose(element, desc):
  return Maker(element, desc, Combiner.choose, 'choose')

_REGISTRY.register(choose)
_REGISTRY.register(inject)
_REGISTRY.register(insert)
_REGISTRY.register(reverse)
_REGISTRY.register(spread)
