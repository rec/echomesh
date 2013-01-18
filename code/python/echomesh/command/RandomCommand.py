from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.thread import TimeLoop
from echomesh.util.math import Poisson

DEFAULT_INTERVAL = 10.0

class RandomCommand(TimeLoop.TimeLoop):
  def __init__(self, parent, element):
    super(RandomCommand, self).__init__(name='RandomCommand')
    se
    self.mean = element.get('data', {}).get('mean', DEFAULT_INTERVAL)
    self.command = element.get('command', {})
    assert self.command['function']

  def _next_time(self, t):
    return t + Poisson.next_poisson(self.mean)

  def _command(self, t):
    self.execute_command(self.command)
