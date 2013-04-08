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
      if k in names:
        v = Expression(v, element)
      self.table[k] = v
    self.function = function
    pattern_desc = desc.get('pattern')
    self.pattern = make_pattern(element, pattern_desc)

  def evaluate(self):
    return self()

  def __call__(self):
    table = dict((k, Call.call(v)) for k, v in self.table.iteritems())
    try:
      del table['pattern']
    except:
      pass

    if self.pattern:
      return self.function(self.pattern(), **table)
    else:
      return self.function(**table)

  def is_constant(self):
    return all(v.is_constant() for v in self.table.itervalues())

def inject(element, desc):
  return Maker(element, desc, Combiner.inject)

def insert(element, desc):
  return Maker(element, desc, Combiner.insert,
                  'length', 'offset', 'rollover', 'skip')

def reverse(element, desc):
  return Maker(element, desc, reversed)

def spread(element, desc):
  return Maker(element, desc, ColorSpread.color_name_spread)

def choose(element, desc):
  pass

_REGISTRY.register(choose)
_REGISTRY.register(inject)
_REGISTRY.register(insert)
_REGISTRY.register(reverse)
_REGISTRY.register(spread)
