from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorSpread
from echomesh.color import Combiner
from echomesh.color import LightSingleton
from echomesh.element import Element
from echomesh.expression.Expression import Expression
from echomesh.util import Call
from echomesh.util import Log
from echomesh.util import Registry

LOGGER = Log.logger(__name__)

_REGISTRY = Registry.Registry('scene types')

def scene(element, description):
  assert description
  return _REGISTRY.get(description.pop('type'))(element, description)

class Functional(object):
  def __init__(self, element, desc, function, *names):
    self.table = {}
    for k, v in desc.iteritems():
      if k in names:
        v = Expression(v, element)
      self.table[k] = v
    self.function = function
    scene_desc = desc.get('scene')
    self.scene = scene_desc and scene(element, scene_desc)

  def evaluate(self):
    return self()

  def __call__(self):
    table = dict((k, Call.call(v)) for k, v in self.table.iteritems())
    try:
      del table['scene']
    except:
      pass

    if self.scene:
      return self.function(self.scene(), **table)
    else:
      return self.function(**table)

  def is_variable(self):
    return any(v.is_variable() for v in self.table.itervalues())

def inject(element, desc):
  return Functional(element, desc, Combiner.inject)

def insert(element, desc):
  return Functional(element, desc, Combiner.insert,
                    'length', 'offset', 'rollover', 'skip')

def reverse(element, desc):
  return Functional(element, desc, reversed)

def spread(element, desc):
  return Functional(element, desc, ColorSpread.color_name_spread)

_REGISTRY.register(inject)
_REGISTRY.register(insert)
_REGISTRY.register(reverse)
_REGISTRY.register(spread)

class Scene(Element.Element):
  def __init__(self, parent, description):
    super(Scene, self).__init__(parent, description)
    assert parent.__class__.__name__ == 'Light'
    self.scene = parent.scenes[description['scene']]

  def _on_run(self):
    super(Scene, self)._on_run()
    LightSingleton.add_client(self.scene)

  def _on_pause(self):
    super(Scene, self)._on_pause()
    LightSingleton.remove_client(self.scene)
