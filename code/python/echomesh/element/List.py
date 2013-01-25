from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.element import Score

class List(Element.Element):
  def __init__(self, parent, description):
    super(Score, self).__init__(parent, description)
    self.element_list = Score.Score(description['elements'])
    self.add_slave(self.element_list)

Element.register(List)
