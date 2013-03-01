from __future__ import absolute_import, division, print_function, unicode_literals

import bisect
import random

from echomesh.element import Element
from echomesh.element import List
from echomesh.element import Load
from echomesh.element import Loop
from echomesh.util.math import Poisson
from echomesh.util.math import Units

class Repeat(Loop.Loop):
  def __init__(self, parent, description):
    super(Repeat, self).__init__(parent, description, name='Repeat')
    self.list_element = List.List(self, description)
    self.random_delay = Units.convert(description.get('random_delay', 0))
    self.period = Units.convert(description.get('period'), 0)
    self.repeat = Units.convert(description.get('repeat', 'infinite'))
    assert self.random_delay > 0 or self.period > 0, (
      'You must set either a period or a random_delay')
    self.add_slave(self.list_element)
    self.repeat_count = 0

  def next_time(self, t):
    res = (self.run_time + self.period * (1 + self.repeat_count))
    if self.random_delay:
      res += Poisson.next_poisson(self.random_delay)
    return res

  def loop_target(self, t):
    self.list_element.run()
    self.repeat_count += 1
    if self.repeat_count >= self.repeat:
      self.stop()

  def child_stopped(self, child):
    pass

  def reset(self):
    self.list_element.reset()

  def class_name(self):
    return self.list_element.class_name(super(Repeat, self).class_name())

Element.register(Repeat)
