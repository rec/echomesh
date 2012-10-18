from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import traceback

from util import Log
from util import Openable

LOGGER = Log.logger(__name__)

class ThreadLoop(Openable.Openable):
  def __init__(self, runnable=None, openable=None):
    Openable.Openable.__init__(self)
    self.openable = openable or self
    if runnable:
      self.runnable = runnable
    self.thread = threading.Thread(target=self.run)

  def start(self):
    self.thread.start()

  def join(self):
    self.thread.join()

  def run(self):
    try:
      while self.is_open:
        self.runnable()
    except:
      print(traceback.format_exc())
      self.close()
