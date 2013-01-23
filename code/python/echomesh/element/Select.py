from __future__ import absolute_import, division, print_function, unicode_literals

import bisect
import random

from echomesh.element import Element
from echomesh.util.math import Poisson
from echomesh.element import Register

DEFAULT_INTERVAL = 10.0

class Select(Element.Element):
  def __init__(self, parent, description):
    super(Select, self).__init__(parent, description, name='SelectCommand')
    self.mean = description.get('mean', DEFAULT_INTERVAL)

    total_weight, weights_counted = 0, 0
    self.elements = []
    weights = []
    for choice in description.get('choices', []):
      weight = choice.get('weight', None)
      if weight is not None:
        assert weight >= 0, "Select weights can't be negative"
        weights_counted += 1
        total_weight += weight
      weights.append(weight)
      self.elements.(Load.make(self, choice['element']))

    if not weights_counted:
      total_weight, weights_counted = 1, 1

    mean_weight = total_weight / weights_counted
    total_weight = 0
    self.totals = []
    for i, w in enumerate(weights):
      total_weight += (mean_weight if w is None else w)
      self.totals.append(total_weight)

  def execute(self):
    rnd = random.random() * self.totals[-1]
    index = bisect.bisect_right(self.totals, rnd)
    element = self.elements(index)
    element.execute()

Register.register(Select)
