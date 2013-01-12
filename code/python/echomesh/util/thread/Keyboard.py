from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time

from echomesh.util.thread import ThreadLoop

CLOSED = False

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
      global CLOSED
      assert not CLOSED

      if not self.processor(raw_input(self.prompt).strip()):
        CLOSED = True
        self.close()
