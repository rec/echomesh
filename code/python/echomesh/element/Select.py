from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.element import Load
from echomesh.util.math.WeightedRandom import WeightedRandom

class Select(Element.Element):
  def __init__(self, parent, description):
    super(Select, self).__init__(parent, description)
    choices = description.get('choices', [])
    self.random = WeightedRandom(c.get('weight', None) for c in choices)
    self.element = [Load.make_one(self, c['element']) for c in choices]
    self.add_stop_only_slave(*self.element)

  def _on_run(self):
    super(Select, self)._on_run()
    self.element[self.random.select()].run()

Element.register(Select)
