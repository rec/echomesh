from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import traceback

from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

class RunnableThread(MasterRunnable):
  def __init__(self, target=None, name=None, report_error=False):
    super(RunnableThread, self).__init__()
    self.name = name or repr(self)
    self.target = target or self.target

  def start(self):
    if not self.is_running:
      super(RunnableThread, self).start()
      self.thread = threading.Thread(target=self._runner)
      self.thread.start()

  def join(self):
    super(RunnableThread, self).join()
    LOGGER.debug('Thread join for "%s"', self.name)
    try:
      self.thread.join()
    except:
      pass

  def _runner(self):
    try:
      self.target()
    except:
      if self.is_running or self.report_error:
        LOGGER.critical(traceback.format_exc())
      self.stop()

