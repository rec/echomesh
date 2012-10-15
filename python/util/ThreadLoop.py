from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from util.Openable import Openable

class ThreadLoop(Openable):
  def __init__(self, runnable=None, openable=None):
    Openable.__init__(self)
    self.openable = openable or self
    if runnable:
      self.runnable = runnable
    self.thread = threading.Thread(target=self.run)
    self.thread.start()

  def run(self):
    try:
      while self.is_open:
        self.runnable()
    except:
      traceback.format_exc()
      self.close()

