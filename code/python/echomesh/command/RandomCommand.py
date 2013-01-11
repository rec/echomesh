from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command.CommandLoop import CommandLoop
from echomesh.util.math import Poisson

DEFAULT_INTERVAL = 10.0

class RandomCommand(CommandLoop):
  def __init__(self, score, element, timeout=None):
    CommandLoop.__init__(self, score, element, timeout)
    self.mean = element.get('data', {}).get('mean', DEFAULT_INTERVAL)
    self.command = element.get('command', {})
    assert self.command['function']

  def _next_time(self, t):
    return t + Poisson.next_poisson(self.mean)

  def _command(self, t):
    self.execute_command(self.command)
