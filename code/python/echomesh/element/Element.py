from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import time

from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util.Registry import Registry

LOGGER = Log.logger(__name__)

class Element(MasterRunnable):
  def __init__(self, parent, description):
    self.parent = parent
    self.description = description
    self.start_time = self.pause_time = 0
    self.load_time = time.time()

    super(Element, self).__init__()

  def reset(self):
    # print('!!! reset', self)
    self.start_time = time.time() - self.pause_time

  def child_paused(self, child):
    self.parent and self.parent.child_paused(child)

  def class_name(self):
    return self.__class__.__name__.lower()

  def time(self):
    if self.is_running:
      return time.time() - self.start_time
    else:
      return self.pause_time

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

  def _on_pause(self):
    super(Element, self)._on_pause()
    self.pause_time = time.time() - self.start_time
    self.child_paused(self)

  def _on_reset(self):
    super(Element, self)._on_reset()
    self.start_time = time.time() - self.pause_time
    self.pause_time = 0

  def info(self):
    return {'class': self.class_name(),
            'state': 'run' if self.is_running else 'pause',
            'time': _format_delta(self.time())}


def _format_delta(t):
  s = str(datetime.timedelta(seconds=t))
  loc = s.find('.')
  if loc > 0:
    s = s[0:loc]
  return s

_REGISTRY = Registry(name='element')

def register(element, name=None):
  _REGISTRY.register(element, name or element.__name__)

get_class_by_name = _REGISTRY.get
