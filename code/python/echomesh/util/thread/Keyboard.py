from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import time

from echomesh.base import Config
from echomesh.command import Command
from echomesh.expression import Expression
from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util.thread.ThreadRunnable import ThreadRunnable

LOGGER = Log.logger(__name__)

USE_RAW_INPUT = not True

MESSAGE = """Type help for a list of commands.
"""

class Keyboard(MasterRunnable):
  def __init__(self, sleep, message, processor,
               prompt='echomesh', sysout=sys.stdout, stdin=sys.stdin):
    super(Keyboard, self).__init__()
    self.sleep = sleep
    self.message = message
    self.processor = processor
    self.prompt = prompt
    self.sysout = sysout
    self.alert_mode = False
    self.stdin = sys.stdin
    self.partial_line = False

  def loop(self):
    self.run()
    while self.is_running:
      self._input_loop()

  def _on_begin(self):
    self.sysout.write('\n')
    self.sysout.flush()
    if self.sleep:
      time.sleep(self.sleep)
      self.sleep = 0
    if self.message:
      print(self.message)
      self.message = ''

  def _input_loop(self):
    buff = ''
    first_time = True
    brackets, braces = 0, 0
    while first_time or brackets > 0 or braces > 0:
      # Keep accepting new lines as long as we have a surplus of open
      # brackets or braces.
      if first_time:
        first_time = False
        self.sysout.write(self.prompt)
      else:
        self.sysout.write(' ' * len(self.prompt))
      self.sysout.write('!' if self.alert_mode else ':')
      self.sysout.write(' ')
      self.sysout.flush()

      data = raw_input() if USE_RAW_INPUT else self.stdin.readline()
      buff += data

      brackets += (data.count('[') - data.count(']'))
      braces += (data.count('{') - data.count('}'))

    if brackets < 0:
      LOGGER.error('Too many ]')
    elif braces < 0:
      LOGGER.error('Too many }')
    elif self.processor(buff.strip()):
      self.pause()


def keyboard(instance, new_thread=True):
  def processor(line):
    try:
      return Command.execute(instance, line)
    except:
      LOGGER.error('Error processing command line.')

  sleep = Expression.convert(Config.get('delay_before_keyboard_activates'))
  keyboard = Keyboard(sleep=sleep, message=MESSAGE, processor=processor)
  if new_thread:
    runnable = ThreadRunnable(target=keyboard.loop)
    runnable.add_mutual_pause_slave(keyboard)
    return runnable

  return keyboard
