from __future__ import absolute_import, division, print_function, unicode_literals

from command.CommandLoop import CommandLoop
from util import Log

LOGGER = Log.logger(__name__)

class SequenceCommand(CommandLoop):
  def __init__(self, score, element, timeout=None):
    CommandLoop.__init__(self, score, element, timeout)
    self.commands = element.get('commands', [])
    self.next_command = 0

  def _command_time(self):
    return self.commands[self.next_command].get('time', 0) + self.start_time

  def _next_time(self, t):
    if self.next_command < len(self.commands):
      return self._command_time()
    else:
      LOGGER.info('Sequence finished')
      self.close()
      return 0

  def _command(self, t):
    while self.next_command < len(self.commands) and self._command_time() <= t:
      LOGGER.info('%d', self.next_command)
      self.execute_command(self.commands[self.next_command])
      self.next_command += 1
