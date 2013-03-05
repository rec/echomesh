from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.element import Load
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class List(Element.Element):
  def __init__(self, parent, description):
    super(List, self).__init__(parent, description)
    element = description.get('element', None)
    if not element:
      raise Exception('In %s, a list must have an element: member.' %
                      self.get_hierarchy_names)
    self.element = Load.make(self, element)
    self.add_slave(*self.element)

  def class_name(self, base_name=''):
    name = base_name or super(List, self).class_name()
    classes = ', '.join(e.class_name() for e in self.element)
    return '%s(%s)' % (name, classes)

  def child_paused(self, child):
    for e in self.element:
      if e.is_running:
        return
    self.pause()

  def reset(self):
    for e in self.element:
      e.reset()

Element.register(List)
