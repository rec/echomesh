from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import traceback

from util import Log
from util.Closer import Closer

LOGGER = Log.logger(__name__)

class ThreadLoop(Closer):
  def __init__(self, run=None, openable=None, name=None,
               report_errors_when_closed=False):
    super(ThreadLoop, self).__init__()
    self.openable = openable or self
    self.name = name or repr(self)
    has_run = getattr(self, 'run', None)
    self.report_errors_when_closed = report_errors_when_closed
    if run:
      assert not has_run
      self.run = run
    else:
      assert has_run

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
      if self.is_open or self.report_errors_when_closed:
        LOGGER.critical(traceback.format_exc())
      self.close()
