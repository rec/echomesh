from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.output.Output import Output
from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

class Poll(ThreadLoop, Output):
  def __init__(self, interval=None, is_daemon=True, name=None, is_redirect=True,
               **description):
    ThreadLoop.__init__(self, is_daemon=is_daemon, name=name)
    Output.__init__(self)
    self.interval = interval
    self.finish_construction(description, is_redirect=is_redirect)

  def _before_thread_start(self):
    self._next_time = time.time()

  def single_loop(self):
    e = self.evaluate()
    if not self.is_running:
      return
    self.emit_output(e)
    if not self.is_running:
      return
    self._next_time += self.interval
    sleep_time = max(0, self._next_time - time.time())
    if sleep_time:
      time.sleep(sleep_time)
