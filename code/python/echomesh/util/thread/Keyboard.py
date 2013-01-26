from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time

from echomesh.command import Processor
from echomesh.base import Config
from echomesh.util.thread import RunnableThread

MESSAGE = """
           echomesh
Type help for a list of commands

"""

class Keyboard(RunnableThread.RunnableThread):
  def __init__(self, sleep, message, processor, prompt='echomesh: '):
    super(Keyboard, self).__init__(name='Keyboard')
    self.sleep = sleep
    self.message = message
    self.processor = processor
    self.prompt = prompt

  def target(self):
    if self.sleep:
      time.sleep(self.sleep)
      self.sleep = 0
    if self.message:
      print(self.message)
      self.message = ''
    while self.is_running:
      if self.processor(raw_input(self.prompt).strip()):
        self.stop()

def keyboard(echomesh):
  if Config.is_control_program():
    processor = Processor.Processor(echomesh).process
    sleep = Config.get('opening_sleep')
    return Keyboard(sleep=sleep, message=MESSAGE, processor=processor)


