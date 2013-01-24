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
