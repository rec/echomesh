from __future__ import absolute_import, division, print_function, unicode_literals

import bisect
import random

from echomesh.element import Element
from echomesh.element import Load
from echomesh.element import Loop
from echomesh.util.math import Poisson
from echomesh.util.math import Units

class Repeat(Loop.Loop):
  def __init__(self, parent, description):
    super(Repeat, self).__init__(parent, description, name='Repeat')
    self.random_delay = Units.convert(description.get('random_delay', 0))
    self.period = Units.convert(description.get('period'), 0)
    assert self.mean > 0 or self.period > 0
    self.element = Load.make_one(self, description['element'])
    self.add_slave(self.element)

  def next_time(self, t):
    res = self.period + t
    if self.random_delay:
      res += Poisson.next_poisson(self.random_delay)
    return res

  def loop_target(self, t):
    self.element.run()

Element.register(Repeat)
