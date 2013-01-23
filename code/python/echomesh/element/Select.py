from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.util.math.WeightedRandom import WeightedRandom
from echomesh.element import Register

class Select(Element.Element):
  def __init__(self, parent, description):
    super(Select, self).__init__(parent, description, name='element.Select')
    choices = description.get('choices', [])
    self.random = WeightedRandom(c.get('weight', None) for c in choices)
    self.elements = [Load.make(self, c['element'] for c in choices)]

  def execute(self):
    return self.elements[self.random.select()].element.execute()

Register.register(Select)
