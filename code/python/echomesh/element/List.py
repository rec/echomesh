from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.element import Load

class List(Element.Element):
  def __init__(self, parent, description):
    super(List, self).__init__(parent, description)
    element = description.get('element', None)
    if not element:
      raise Exception('In %s, a list must have an element: member.' %
                      self.get_hierarchy_names)
    self.element = Load.make(parent, element)
    self.add_slave(*self.element)

  def child_stopped(self, child):
    for e in self.element:
      if e.is_running:
        return
    self.stop()

Element.register(List)
