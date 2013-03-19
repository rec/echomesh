from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.element import Loop
from echomesh.util.math import Poisson
from echomesh.util.math import Units

class Repeat(Loop.Loop):
  def __init__(self, parent, description):
    super(Repeat, self).__init__(parent, description, name='Repeat')
    self.random_delay = Units.convert(description.get('random_delay', 0))
    self.period = Units.convert(description.get('period'), 0)
    self.repeat = Units.convert(description.get('repeat', 'infinite'))
    assert self.random_delay > 0 or self.period > 0, (
      'You must set either a period or a random_delay')
    self.repeat_count = 0

  def next_time(self, t):
    start = self.start_time
    res = start + self.period * (1 + self.repeat_count)
    if self.random_delay:
      res += Poisson.next_poisson(self.random_delay)
    return res

  def loop_target(self, t):
    for e in self.elements:
      e.reset()
      e.start()

    self.repeat_count += 1
    if self.repeat_count >= self.repeat:
      self.pause()

  def child_paused(self, child):
    pass

  def reset(self):
    self.repeat_count = 0
    for e in self.elements:
      e.reset()

Element.register(Repeat)
