from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time

from echomesh.util.thread import ThreadLoop

class Keyboard(ThreadLoop.ThreadLoop):
  def __init__(self, parent, sleep, message, processor, prompt='echomesh: '):
    super(Keyboard, self).__init__()
    self.parent = parent
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
