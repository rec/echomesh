from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import threading
import time

from echomesh.base import Config
from echomesh.command import Command
from echomesh.util.math import Units
from echomesh.util.thread import ThreadRunnable

MESSAGE = """Type help for a list of commands.
"""

class Keyboard(ThreadRunnable.ThreadRunnable):
  def __init__(self, sleep, message, processor,
               prompt='echomesh', output=sys.stdout):
    super(Keyboard, self).__init__(name='Keyboard')
    self.sleep = sleep
    self.message = message
    self.processor = processor
    self.prompt = prompt
    self.output = output
    self.alert_mode = False

  def target(self):
    self._begin()
    while self.is_running:
      self._input_loop()

  def _begin(self):
    self.output.write('\n')
    self.output.flush()
    if self.sleep:
      time.sleep(self.sleep)
      self.sleep = 0
    if self.message:
      print(self.message)
      self.message = ''

  def _input_loop(self):
    buffer = ''
    first_time = True
    brackets, braces = 0, 0
    while first_time or brackets > 0 or braces > 0:
      # Keep accepting new lines as long as we have a surplus of open
      # brackets or braces.
      if first_time:
        first_time = False
        self.output.write(self.prompt)
      else:
        self.output.write(' ' * len(self.prompt))
      self.output.write('!' if self.alert_mode else ':')
      self.output.write(' ')
      self.output.flush()

      data = raw_input()
      buffer += data

      brackets += (data.count('[') - data.count(']'))
      braces += (data.count('{') - data.count('}'))

    if brackets < 0:
      LOGGER.error('Too many ]')
    elif braces < 0:
      LOGGER.error('Too many }')
    elif self.processor(buffer.strip()):
      self.stop()

def keyboard(echomesh):
  if Config.get('control_program', 'enable'):
    processor = lambda line: Command.execute(echomesh, line)
    sleep = Units.get_config('delay_before_keyboard_activates')
    return Keyboard(sleep=sleep, message=MESSAGE, processor=processor)
