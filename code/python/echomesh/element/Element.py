from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import time

from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util.Registry import Registry

LOGGER = Log.logger(__name__)

class Element(MasterRunnable):
  def __init__(self, parent, description, full_slave=True):
    self.start_time = self.pause_time = 0
    self.parent = parent
    self.description = description
    self.load_time = time.time()
    super(Element, self).__init__()

    elements = description.get('elements', None)
    if elements:
      # This has to be local to avoid an infinite loop...
      # pylint: disable=R0401
      from echomesh.element import Load
      # pylint: enable=R0401

      self.elements = Load.make(self, elements)
      if full_slave:
        self.add_slave(*self.elements)
      else:
        self.add_pause_only_slave(*self.elements)
    else:
      self.elements = []

  def child_paused(self, _child):
    for e in self.elements:
      if e.is_running:
        return

    self.pause()

  def class_name(self):
    name = self.__class__.__name__.lower()
    if self.elements:
      classes = ', '.join(e.class_name() for e in self.elements)
      return '%s(%s)' % (name, classes)
    else:
      return name

  def elapsed_time(self):
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

  def get_hierarchy(self, so_far=None):
    res = (so_far or []) + [self]
    return self.parent.get_hierarchy(res) if self.parent else res

  def get_hierarchy_names(self):
    h = self.get_hierarchy()
    return ': '.join(n.__class__.__name__.lower() for n in h)

  def _on_pause(self):
    super(Element, self)._on_pause()
    self.pause_time = time.time() - self.start_time
    if self.parent:
      self.parent.child_paused(self)

  def _on_reset(self):
    super(Element, self)._on_reset()
    self.start_time = time.time() - self.pause_time
    self.pause_time = 0

  def info(self):
    return {'class': self.class_name(),
            'state': 'run' if self.is_running else 'pause',
            'time': _format_delta(self.elapsed_time())}


def _format_delta(t):
  s = str(datetime.timedelta(seconds=t))
  loc = s.find('.')
  if loc > 0:
    s = s[0:loc]
  return s

REGISTRY = Registry(name='element')

def register(element, name=None):
  REGISTRY.register(element, name or element.__name__)

get_class_by_name = REGISTRY.get
