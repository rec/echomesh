from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.element.Loop import Loop
from echomesh.expression import UnitConfig
from echomesh.expression import Expression
from echomesh.util.math import Poisson

class Repeat(Loop):
  def __init__(self, parent, description, name='Repeat', **kwds):
    super(Repeat, self).__init__(parent, description, name, **kwds)
    self.random_delay = Expression.convert(description.get('random_delay', 0))
    self.period = Expression.convert(description.get('period', 0))
    self.repeat = Expression.convert(description.get('repeat', 'infinite'))
    assert self.random_delay > 0 or self.period > 0, (
      'You must set either a period or a random_delay')

  def _on_begin(self):
    super(Repeat, self)._on_begin()
    self.repeat_count = 0

  def next_time(self, t):
    speed = UnitConfig.get('speed')
    t += self.period / speed
    if self.random_delay:
      t += Poisson.next_poisson(self.random_delay) / speed
    return t

  def loop_target(self, t):
    for e in self.elements:
      e.start()

    self.repeat_count += 1
    if self.repeat_count >= self.repeat:
      self.pause()

  def child_paused(self, child):
    pass

  def _on_begin(self):
    super(Repeat, self)._on_begin()
    self.repeat_count = 0
