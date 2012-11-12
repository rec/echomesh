from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import traceback

from util import Log
from util.Openable import Openable

LOGGER = Log.logger(__name__)

class ThreadLoop(Openable):
  def __init__(self, run=None, openable=None, name=None):
    super(ThreadLoop, self).__init__()
    self.openable = openable or self
    self.name = name or repr(self)
    if run:
      assert not getattr(self, 'run', None)
      self.run = run

  def start(self):
    LOGGER.debug('starting %s', self.name)
    self.thread = threading.Thread(target=self.loop)
    self.thread.start()

  def join(self):
    try:
      self.thread.join()
    except:
      pass  # Swallow errors!  TODO

  def close(self):
    super(ThreadLoop, self).close()
    LOGGER.debug('closing %s', self.name)

  def loop(self):
    try:
      while self.is_open:
        self.run()
    except:
      LOGGER.critical(traceback.format_exc())
