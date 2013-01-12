from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.thread.TimeLoop import TimeLoop

class CommandLoop(TimeLoop):
  def __init__(self, score, element, timeout=None, name='CommandLoop'):
    TimeLoop.__init__(self, timeout, name=name)
    self.score = score
    self.element = element

  def execute_command(self, command):
    self.score.execute_command(command)
