from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.util import Log
from echomesh.util.thread import ThreadLoop

LOGGER = Log.logger(__name__)

DEFAULT_TIMEOUT = 0.5

class TimeLoop(ThreadLoop.ThreadLoop):
  def __init__(self, timeout=None, name='TimeLoop', interval=1):
    super(TimeLoop, self).__init__(name=name)
    self.timeout = timeout or DEFAULT_TIMEOUT
    self.interval = interval

  def start(self):
    self.start_time = time.time()
    self.next_time = self.start_time
    super(TimeLoop, self).start()

  def run(self):
    t = time.time()
    if t >= self.next_time:
      self._command(t)
      self.next_time = self._next_time(t)
    if self.is_open:
      time.sleep(min(DEFAULT_TIMEOUT, self.next_time - t))

  def _next_time(self, t):
    return t + self.interval

  def _command(self, t):
    raise Exception('You must implement _event in your derived class')

