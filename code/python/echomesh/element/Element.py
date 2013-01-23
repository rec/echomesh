from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Load
from echomesh.util import Log
from echomesh.util.thread import Closer
from echomesh.util.thread import TimeLoop

LOGGER = Log.logger(__name__)

class Element(Closer.Closer):
  def __init__(self, parent, description):
    super(Element, self).__init__()
    self.parent = parent
    self.description = description
    self.element = self

  def execute(self):
    pass

  def read_repeated(self, name):
    elements = []
    desc = self.description.get(name, None)
    if desc:
      try:
        elements = Load.make(self, desc)
      except:
        LOGGER.error("Couldn't read element description named %s from %s",
                     name, desc)
    setattr(self, name, elements)
    self.add_openable(*elements)


class Loop(TimeLoop.TimeLoop):
  def __init__(self, parent, description, name='Element.Loop'):
    super(Loop, self).__init__(name=name)
    self.element = Element(parent, description)
    self.add_openable_mutual(self.element)

