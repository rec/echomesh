from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.util import Log
from echomesh.util.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

DEFAULT_TIMEOUT = 0.5

class TimeLoop(ThreadLoop):
  def __init__(self, timeout=None):
    ThreadLoop.__init__(self)
    self.timeout = timeout or DEFAULT_TIMEOUT

  def start(self):
    self.start_time = time.time()
    self.next_time = self._next_time(self.start_time)
    ThreadLoop.start(self)

  def run(self):
    t = time.time()
    if t >= self.next_time:
      self._command(t)
      self.next_time = self._next_time(t)
    if self.is_open:
      time.sleep(min(DEFAULT_TIMEOUT, self.next_time - t))

  def _command(self, t):
    raise Exception('You must implement _event in your derived class')

  def _next_time(self, t):
    raise Exception('You must implement _next_time in your derived class')


