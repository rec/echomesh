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
    self.elements = make(self, description.get('elements', []))
    self.add_openable(*self.elements)
    self.element = self

class Loop(TimeLoop.TimeLoop):
  def __init__(self, parent, description, name='Element.Loop'):
    super(Loop, self).__init__(name=name)
    self.element = Element(parent, description)
    self.add_openable_mutual(self.element)
