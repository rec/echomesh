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

  def _init_loop(self):
    self.buff = ''
    self.first_time = True
    self.brackets, self.braces = 0, 0

  def _input_loop(self):
    self._init_loop()

    while self.first_time or self.brackets > 0 or self.braces > 0:
      # Keep accepting new lines as long as we have a surplus of open
      # self.brackets or self.braces.

      self._prompt()
      self.receive_data(self.stdin.readline())

    if self.brackets < 0:
      LOGGER.error('Too many ]')
    elif self.braces < 0:
      LOGGER.error('Too many }')
    elif self.processor(self.buff.strip()):
      self.pause()

  def _prompt(self):
    if self.first_time:
      self.first_time = False
      self.sysout.write(self.prompt)
    else:
      self.sysout.write(' ' * len(self.prompt))
    self.sysout.write('!' if self.alert_mode else ':')
    self.sysout.write(' ')
    self.sysout.flush()

  def receive_data(self, data):
    self.buff += data

    self.brackets += (data.count('[') - data.count(']'))
    self.braces += (data.count('{') - data.count('}'))


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
