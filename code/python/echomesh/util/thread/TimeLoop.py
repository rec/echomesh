from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.util import Log
from echomesh.util.thread import ThreadLoop

DEFAULT_TIMEOUT = 0.5
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

    assert self.loop_target
    assert self.next_time

  def _on_start(self):
    self.start_time = time.time()
    self.next_loop_time = self.start_time

  def one_loop(self):
    t = self.timer()
    if t >= self.next_loop_time:
      self.loop_target(t)
      self.next_loop_time = self.next_time(self.next_loop_time)
      if self.next_loop_time <= t:
        self.next_loop_time = self.next_time(t)

    if self.is_running:
      self.sleep(min(DEFAULT_TIMEOUT, self.next_loop_time - t))

  def next_time(self, t):
    return t + self.interval

  def loop(self, t):
    pass

