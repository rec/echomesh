from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import traceback

from util import Log
from util import Openable

LOGGER = Log.logger(__name__)

class ThreadLoop(Openable.Openable):
  def __init__(self, run=None, openable=None):
    Openable.Openable.__init__(self)
    self.openable = openable or self
    if run:
      assert not getattr(self, 'run', None)
      self.run = run

  def start(self):
    self.thread = threading.Thread(target=self.loop)
    self.thread.start()

  def join(self):
    try:
      self.thread.join()
    except:
      pass  # Swallow errors!  TODO

  def loop(self):
    try:
      while self.is_open:
        self.run()
    except:
      LOGGER.critical(traceback.format_exc())
      self.close()
