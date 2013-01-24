from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.util import Log
from echomesh.util.thread import ThreadLoop

LOGGER = Log.logger(__name__)

DEFAULT_TIMEOUT = 0.5

class TimeLoop(ThreadLoop.ThreadLoop):
  def __init__(self, timeout=None, name='TimeLoop', interval=1,
               next_time=None, loop=None):
    super(TimeLoop, self).__init__(name=name)
    self.timeout = timeout or DEFAULT_TIMEOUT
    self.interval = interval
    self.loop = loop or self.loop
    self.next_time = next_time or self.next_time

  def start(self):
    self.start_time = time.time()
    self.next_loop_time = self.start_time
    super(TimeLoop, self).start()

  def target(self):
    t = time.time()
    if t >= self.next_loop_time:
      self.loop(t)
      self.next_loop_time = self.next_time(self.next_loop_time)
      if self.next_loop_time <= t:
        self.next_loop_time = self.next_time(t)

    if self.is_running:
      time.sleep(min(DEFAULT_TIMEOUT, self.next_time - t))

  def next_time(self, t):
    return t + self.interval

  def loop(self, t):
    pass

