from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

class ThreadRunnable(MasterRunnable):
  def __init__(self, target=None, name=None, report_error=False):
    super(ThreadRunnable, self).__init__()
    self.name = name or repr(self)
    self._target = target or self.target
    self.report_error = report_error

  def target(self):
    pass

  def _on_run(self):
    def target():
      try:
        self._target()
      except Exception:
        if self.is_running or self.report_error:
          LOGGER.error('Thread %s reports an error:', self.name, exc_info=1)
        self.pause()
      self._after_thread_pause()

    super(ThreadRunnable, self)._on_run()
    self._before_thread_start()
    self.thread = threading.Thread(target=target, name=self.name)
    self.thread.daemon = True
    self.thread.start()

  def _before_thread_start(self):
    pass

  def _after_thread_pause(self):
    pass
