from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorSpread
from echomesh.color import Combiner
from echomesh.expression.Expression import Expression
from echomesh.util import Call
from echomesh.util import Registry

_REGISTRY = Registry.Registry('pattern types')

def make_renderer(element, description):
  return _REGISTRY.get(description.pop('type'))(element, description)

def make_renderers(element, description):
  result = {}
  for k, v in description.iteritems():
    result[k] = make_renderer(element, v)
  return result

class Renderer(object):
  def __init__(self, element, desc, function, *names):
    self.table = {}
    for k, v in desc.iteritems():
      if k in names:
        v = Expression(v, element)
      self.table[k] = v
    self.function = function
    pattern_desc = desc.get('pattern')
    self.pattern = pattern_desc and make_renderer(element, pattern_desc)

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
  return Renderer(element, desc, Combiner.inject)

def insert(element, desc):
  return Renderer(element, desc, Combiner.insert,
                    'length', 'offset', 'rollover', 'skip')

def reverse(element, desc):
  return Renderer(element, desc, reversed)

def spread(element, desc):
  return Renderer(element, desc, ColorSpread.color_name_spread)

_REGISTRY.register(inject)
_REGISTRY.register(insert)
_REGISTRY.register(reverse)
_REGISTRY.register(spread)
