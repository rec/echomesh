from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import threading
import time

from echomesh.command import Processor
from echomesh.base import Config
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
    processor = Processor.Processor(echomesh)
    sleep = Config.get('opening_sleep')
    return Keyboard(sleep=sleep, message=MESSAGE, processor=processor)
