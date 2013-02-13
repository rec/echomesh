from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import threading
import time

from echomesh.base import Config
from echomesh.command import Command
from echomesh.util.thread import ThreadRunnable

MESSAGE = """Type help for a list of commands.
"""

class Keyboard(ThreadRunnable.ThreadRunnable):
  def __init__(self, sleep, message, processor, prompt='echomesh: ', output=sys.stdout):
    super(Keyboard, self).__init__(name='Keyboard')
    self.sleep = sleep
    self.message = message
    self.processor = processor
    self.prompt = prompt
    self.output = output

  def target(self):
    self.output.write('\n')
    self.output.flush()
    if self.sleep:
      time.sleep(self.sleep)
      self.sleep = 0
    if self.message:
      print(self.message)
      self.message = ''
    while self.is_running:
      self.output.write(self.prompt)
      self.output.flush()
      if self.processor(raw_input().strip()):
        self.stop()

def keyboard(echomesh):
  if Config.is_control_program():
    processor = lambda line: Command.execute(echomesh, line)
    sleep = Config.get('opening_sleep')
    return Keyboard(sleep=sleep, message=MESSAGE, processor=processor)
