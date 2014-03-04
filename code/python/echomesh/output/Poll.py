from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.output.Output import Output
from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

class Poll(Output):
  def __init__(
      self, period=None, is_daemon=True, name=None, is_redirect=True, **desc):
    self.thread_loop = ThreadLoop(
      is_daemon=is_daemon, name=name, single_loop=self.single_loop)
    super(Poll, self).__init__()
    self.add_mutual_pause_slave(self.thread_loop)
    self.period = period
    self.finish_construction(desc, is_redirect=is_redirect)

  def _on_run(self):
    self._next_time = time.time()

  def single_loop(self):
    e = self.evaluate()
    if not self.is_running:
      return
    self.emit_output(e)
    if not self.is_running:
      return
    self._next_time += self.period
    sleep_time = max(0, self._next_time - time.time())
    if sleep_time:
      time.sleep(sleep_time)
