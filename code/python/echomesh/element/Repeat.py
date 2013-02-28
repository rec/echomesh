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
    assert self.random_delay > 0 or self.period > 0
    self.add_slave(self.list_element)
    self.stop_time = 0
    self.repeat_count = 0

  def next_time(self, t):
    res = self.period + t - self.stop_time
    self.stop_time = 0
    if self.random_delay:
      res += Poisson.next_poisson(self.random_delay)
    return res

  def loop_target(self, t):
    print('!!!')
    self.list_element.run()
    self.repeat_count += 1
    if self.repeat_count >= self.repeat:
      self.stop()

  def child_stopped(self, child):
    pass

Element.register(Repeat)
