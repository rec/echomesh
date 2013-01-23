from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Load
from echomesh.util import Log
from echomesh.util.thread import Closer

LOGGER = Log.logger(__name__)

class Element(Closer.Closer):
  def __init__(self, parent, description):
    super(Element, self).__init__()
    self.parent = parent
    self.description = description

  # TODO: remove?
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

