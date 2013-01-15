from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time

from echomesh.command import Processor
from echomesh.config import Config
from echomesh.util.thread import ThreadLoop

MESSAGE = """
           echomesh
Type help for a list of commands

"""

class Keyboard(ThreadLoop.ThreadLoop):
  def __init__(self, parent, sleep, message, processor, prompt='echomesh: '):
    super(Keyboard, self).__init__(parent=parent, name='Keyboard')
    self.sleep = sleep
    self.message = message
    self.processor = processor
    self.prompt = prompt

  def run(self):
    if self.sleep:
      time.sleep(self.sleep)
      self.sleep = 0
    if self.message:
      print(self.message)
      self.message = ''
    while self.is_open:
      if not self.processor(raw_input(self.prompt).strip()):
        self.close()

def keyboard(echomesh):
  if Config.is_control_program():
      processor = lambda x: Processor.process(x, echomesh)
      return Keyboard(parent=echomesh,
                      sleep=Config.get('opening_sleep'),
                      message=MESSAGE,
                      processor=processor)

