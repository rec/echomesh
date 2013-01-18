from __future__ import absolute_import, division, print_function, unicode_literal

from echomesh.util.thread import Closer
from echomesh.util.thread import TimeLoop
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Element(Closer.Closer):
  def __init__(self, parent, description):
    super(Element, self).__init__()
    self.parent = parent
    self.description = description
    self.elements = list(make(self, description.get('elements', [])))
    self.add_openable(*self.elements)
    self.element = self

class Loop(TimeLoop.TimeLoop):
  def __init__(self, parent, description, name='Element.Loop'):
    super(Loop, self).__init__(name=name)
    self.element = Element(parent, description)
    self.add_openable_mutual(self.element)

ELEMENT_MAKERS = {}

def register(element_maker, name=None):
  name = name or element_maker.__name__
  old_maker = ELEMENT_MAKERS.get(name, None)
  if old_maker is not element_maker:
    if old_maker:
      raise Exception('Duplicate function name %s' % name)
    ELEMENT_MAKERS[name] = element_maker

def make(parent, description):
  t = description.get('type', None)
  if t:
    maker = ELEMENT_MAKERS.get(t), None)
    if maker:
      return maker(parent, description)
    else:
      LOGGER.error("Didn't understand type %s", t)
  else:
    LOGGER.error("Element description had no type: '%s'", description)

