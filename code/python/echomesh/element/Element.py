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

  def child_stopped(self, child):
    pass

  def _on_stop(self):
    self.parent and self.parent.child_stopped(self)

  def get_property(self, name, default=None):
    none = object()
    prop = getattr(self, name, none)
    return (prop if prop is not none
            else self.parent.get_property(name, default) if self.parent
            else default)

  def get_hierarchy(self, so_far=[]):
    res = so_far + [self]
    return self.parent.get_hierarchy(res) if self.parent else res

  def get_hierarchy_names(self):
    h = self.get_hierarchy()
    return ': '.join(n.__class__.__name__.lower() for n in h)

_REGISTRY = Registry(name='element')

def register(element, name=None):
  _REGISTRY.register(element, name or element.__name__)

get_class_by_name = _REGISTRY.get
