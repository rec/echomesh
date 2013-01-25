from __future__ import absolute_import, division, print_function, unicode_literals

import bisect
import random

from echomesh.element import Load
from echomesh.element import Loop
from echomesh.element import Register
from echomesh.util.math import Poisson

DEFAULT_INTERVAL = 10.0

class Random(Loop.Loop):
  def __init__(self, parent, description):
    super(Random, self).__init__(parent, description, name='Random')
    self.mean = description.get('mean', DEFAULT_INTERVAL)
    self.element = Load.make_one(self, description['element'])
    self.add_slave(self.element)

  def next_time(self, t):
    return t + Poisson.next_poisson(self.mean)

  def loop(self, t):
    self.element.start()

Register.register(Random)