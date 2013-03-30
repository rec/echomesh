from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorSpread
from echomesh.color import Light
from echomesh.expression.Expression import Expression
from echomesh.util import Log
from echomesh.util import Registry

LOGGER = Log.logger(__name__)

_REGISTRY = Registry.Registry('scene types')

def scene(element, description):
  assert description
  return _REGISTRY.get(description.pop('type'))(element, description)

class Functional(object):
  def __init__(self, element, desc, function, *names):
    self.table = dict((k, Expression(desc.get(k), element)) for k in names)
    self.function = function
    scene_desc = desc.get('scene')
    self.scene = scene_desc and scene(element, scene_desc)

  def evaluate(self):
    table = dict((k, v.evaluate()) for k, v in self.table.iteritems())
    if self.scene:
      return self.function(self.scene.evaluate(), **table)
    else:
      return self.function(**table)

  def is_variable(self):
    return any(v.is_variable() for v in self.table.itervalues())

def inject(element, desc):
  return Functional(element, desc, Light.inject)

def insert(element, desc):
  return Functional(element, desc, Light.insert,
                    'length', 'offset', 'rollover', 'skip')

def reverse(element, desc):
  return Functional(element, desc, reversed)

def spread(element, desc):
  return Functional(element, desc, ColorSpread.color_name_spread)

_REGISTRY.register(inject)
_REGISTRY.register(insert)
_REGISTRY.register(reverse)
_REGISTRY.register(spread)
