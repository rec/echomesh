from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util.Registry import Registry

LOGGER = Log.logger(__name__)

class Element(MasterRunnable):
  def __init__(self, parent, description):
    super(Element, self).__init__()
    self.parent = parent
    self.description = description

_REGISTRY = Registry(name='element')

def register(element, name=None):
  _REGISTRY.register(element, name or element.__name__)

get_element_by_name = _REGISTRY.get
