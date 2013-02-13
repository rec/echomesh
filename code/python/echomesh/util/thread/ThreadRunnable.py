from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

class ThreadRunnable(MasterRunnable):
  def __init__(self, target=None, name=None, report_error=False):
    super(ThreadRunnable, self).__init__()
    self.name = name or repr(self)
    self.target = target or self.target
    self.report_error = report_error

  def _on_start(self):
    def target():
      try:
        self.target()
      except Exception as e:
        if self.is_running or self.report_error:
          Log.exception(LOGGER, e)
        self.stop()
    self.thread = threading.Thread(target=target)
    self.thread.daemon = True
    self.thread.start()

  def _on_stop(self):
    self.thread.stop()

  def join(self):
    super(ThreadRunnable, self).join()
    LOGGER.debug('Thread join for "%s"', self.name)
    try:
      self.thread.join()
    except:
      pass


