from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.output.Output import Output
from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

class Poll(Output, ThreadLoop):
  def __init__(self, interval=None, is_daemon=True, name=None, **description):
    Output.__init__(self)
    ThreadLoop.__init__(self, is_daemon=is_daemon, name=name)
    if not interval or interval < 0:
      raise Exception('You need an interval for a Poll Output')
    self.interval = interval
    self.finish_construction(description)

  def _before_thread_start(self):
    self._next_time = time.time()

  def _after_thread_pause(self):
    self.clear()

  def single_loop(self):
    e = self.evaluate()
    if not self.is_running:
      return
    self.emit_output(e)
    if not self.is_running:
      return
    self._next_time += period
    sleep_time = max(0, self._next_time - time.time())
    if sleep_time:
      time.sleep(sleep_time)
