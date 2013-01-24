from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Loop
from echomesh.element import Register
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Sequence(Loop.Loop):
  def __init__(self, parent, description):
    super(Sequence, self).__init__(parent, description, name='Sequence')
    # TODO: fix this

  def _command_time(self):
    return self.commands[self.next_command].get('time', 0) + self.start_time

  def _next_time(self, t):
    if self.next_command < len(self.commands):
      LOGGER.debug('Running command %d', self.next_command)
      return self._command_time()
    else:
      LOGGER.debug('Sequence finished')
      self.stop()
      return 0

  def _loop(self, t):
    while self.next_command < len(self.commands) and self._command_time() <= t:
      LOGGER.debug('%d', self.next_command)
      self.execute_command(self.commands[self.next_command])
      self.next_command += 1

Register.register(Sequence)
