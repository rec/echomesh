from __future__ import absolute_import, division, print_function, unicode_literals

from util.TimeLoop import TimeLoop

class CommandLoop(TimeLoop):
  def __init__(self, score, element, timeout=None):
    TimeLoop.__init__(self, timeout)
    self.score = score
    self.element = element

  def execute_command(self, command):
    self.score.execute_command(command)
