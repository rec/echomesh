from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import traceback

from echomesh.util import Log
from echomesh.util.thread.Closer import Closer

LOGGER = Log.logger(__name__)

class ThreadLoop(Closer):
  def __init__(self, run=None, parent=None, name=None,
               report_errors_when_closed=False):
    super(ThreadLoop, self).__init__(parent=parent)
    self.name = name or repr(self)
    has_run = getattr(self, 'run', None)
    self.report_errors_when_closed = report_errors_when_closed
    if run:
      assert not has_run
      self.run = run
    else:
      assert has_run

  def start(self):
    super(ThreadLoop, self).start()
    self.thread = threading.Thread(target=self.loop)
    self.thread.start()

  def join(self):
    super(ThreadLoop, self).join()
    LOGGER.debug('Thread join for "%s"', self.name)
    try:
      self.thread.join()
    except:
      pass  # Swallow errors!  TODO

  def loop(self):
    try:
      while self.is_open:
        self.run()
      LOGGER.debug('Loop for "%s" has finished', self.name)
    except:
      if self.is_open or self.report_errors_when_closed:
        LOGGER.critical(traceback.format_exc())
      self.close()
