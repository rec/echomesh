from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.util import Log
from echomesh.util.thread import ThreadLoop

# TODO: these should be config values.

DEFAULT_TIMEOUT = 1.0
DEFAULT_INTERVAL = 1.0

class TimeLoop(ThreadLoop.ThreadLoop):
  def __init__(self,
               interval=DEFAULT_INTERVAL,
               loop_target=None,
               name='TimeLoop',
               next_time=None,
               sleep=time.sleep,
               timeout=DEFAULT_TIMEOUT,
               timer=time.time):
    super(TimeLoop, self).__init__(name=name)
    self.interval = interval
    self.loop_target = loop_target or self.loop_target
    self.next_time = next_time or self.next_time
    self.sleep = sleep
    self.timeout = timeout
    self.timer = timer
    self.stop_time = 0

    assert self.loop_target
    assert self.next_time

  def _before_thread_start(self):
    self.start_time = time.time() - self.stop_time
    self.next_loop_time = self.start_time

  def single_loop(self):
    t = self.timer()
    if t >= self.next_loop_time:
      self.loop_target(t)
      self.next_loop_time = self.next_time(self.next_loop_time)
      if self.next_loop_time <= t:
        self.next_loop_time = self.next_time(t)

    if self.is_running:
      sleep_time = min(DEFAULT_TIMEOUT, self.next_loop_time - t)
      self.sleep(sleep_time)

  def next_time(self, t):
    return t + self.interval

  def _after_thread_stop(self):
    self.stop_time = time.time() - self.start_time
