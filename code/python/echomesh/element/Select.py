from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.util import Log
from echomesh.util.math.WeightedRandom import WeightedRandom

LOGGER = Log.logger(__name__)

class Select(Element.Element):
  def __init__(self, parent, description):
    super(Select, self).__init__(parent, description, full_slave=False)
    assert self.elements
    weights = description.get('weights', [])
    wlen, elen = len(weights), len(self.elements)
    if wlen > elen:
      LOGGER.error('More weights than elements: %d > %d',
                   wlen, elen)
      weights = weights[0:elen]

    elif wlen < elen:
      if wlen:
        mean = sum(*weights) / wlen
      else:
        mean = 1
      weights.extend([mean] * (elen - wlen))

    self.random = WeightedRandom(weights)

  def _on_run(self):
    super(Select, self)._on_run()
    if self.elements:
      self.elements[self.random.select()].run()

Element.register(Select)
