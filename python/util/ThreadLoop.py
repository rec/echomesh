from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from util.Openable import Openable

class ThreadLoop(Openable):
  def __init__(self, runnable):
    Openable.__init__(self)
    self.runnable = runnable
    self.thread = threading.Thread(target=self.run)
    self.thread.start()

  def run(self):
    while self.is_open:
      self.runnable()
