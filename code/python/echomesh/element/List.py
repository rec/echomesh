from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.element import Root

# TODO: fix or delete this.
class List(Element.Element):
  def __init__(self, parent, description):
    super(List, self).__init__(parent, description)
    self.element_list = Root.Root(description['elements'])
    self.add_slave(self.element_list)

Element.register(List)
