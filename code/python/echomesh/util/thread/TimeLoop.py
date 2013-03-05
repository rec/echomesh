from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.util import Log
from echomesh.util.thread import ThreadLoop
from echomesh.util.math.Units import INFINITY

# TODO: these should be config values.

DEFAULT_TIMEOUT = 1.0
DEFAULT_INTERVAL = INFINITY

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

    if loop_target:
      self.loop_target = loop_target

    if next_time:
      self.next_time = next_time

    self.sleep = sleep
    self.timeout = timeout
    self.timer = timer
    self.pause_time = 0

    assert self.loop_target
    assert self.next_time

  def _before_thread_start(self):
    self.start_time = self.timer() - self.pause_time
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
      if sleep_time > 0:
        self.sleep(sleep_time)
      else:
        LOG.error('Sleeping for negative time %s', sleep_time, limit=10)

  def next_time(self, t):
    return t + self.interval

  def _after_thread_pause(self):
    self.pause_time = self.timer() - self.start_time
