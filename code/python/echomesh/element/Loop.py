from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.element import Element
from echomesh.util import Log
from echomesh.util.math.Units import INFINITY
from echomesh.util.thread import ThreadLoop

LOGGER = Log.logger(__name__)

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
    self.load_time = timer()

  def _before_thread_start(self):
    t = self.timer()
    self.start_time = t - self.pause_time
    self.next_loop_time = self.next_time(t)
    print('!!!! 1', self.start_time - self.load_time,
          self.next_loop_time - self.load_time)

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
        LOGGER.error('Sleeping for negative time %s', sleep_time, limit=10)

  def next_time(self, t):
    return t + self.interval

  def _after_thread_pause(self):
    self.pause_time = self.timer() - self.start_time
    print('!!!! 2', self.pause_time)


class Loop(Element.Element):
  def __init__(self, parent, description, interval=1, name='Element.Loop'):
    super(Loop, self).__init__(parent, description)
    self.time_loop = TimeLoop(
      name=name,
      interval=interval,
      next_time=getattr(self, 'next_time', None),
      loop_target=getattr(self, 'loop_target', None))

    self.add_slave(self.time_loop)
    self.time_loop.add_pause_only_slave(self)

  # You can implement Loop.next_time and Loop.loop_target to override the
  # methods in TimeLoop.
