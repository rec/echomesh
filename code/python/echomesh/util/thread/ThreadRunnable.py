from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

class ThreadRunnable(MasterRunnable):
  def __init__(self, target=None, name=None, report_error=False):
    super(ThreadRunnable, self).__init__()
    self.name = name or repr(self)
    if target:
      self.target = target
    else:
      assert self.target
    self.report_error = report_error

  def _on_run(self):
    self._before_thread_start()
    def target():
      try:
        self.target()
      except Exception as e:
        if self.is_running or self.report_error:
          LOGGER.error('Uncaught thread error', exc_info=1)
        self.stop()
    self.thread = threading.Thread(target=target)
    self.thread.daemon = True
    self.thread.start()

  def _on_stop(self):
    self.thread.stop()
    self._after_thread_stop()

  def _before_thread_start(self):
    pass

  def _after_thread_stop(self):
    pass
