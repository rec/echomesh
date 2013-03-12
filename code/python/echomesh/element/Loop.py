from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time

from echomesh.element import Element
from echomesh.util import Log
from echomesh.util.math.Units import INFINITY
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

# TODO: these should be config values.
DEFAULT_TIMEOUT = 1.0
DEFAULT_INTERVAL = INFINITY

class TimeLoop(MasterRunnable):
  def __init__(self,
               interval=DEFAULT_INTERVAL,
               loop_target=None,
               name='TimeLoop',
               next_time=None,
               report_error_on_close=False,
               timeout=DEFAULT_TIMEOUT):
    super(TimeLoop, self).__init__()
    self.name = name or repr(self)
    self.report_error_on_close = report_error_on_close
    self.interval = interval
    self.next_time = next_time
    self.loop_target = loop_target

    self.timeout = timeout
    self.pause_time = 0
    self.load_time = time.time()

  def target(self):
    while self.is_running:
      try:
        self.single_loop()
      except Exception as e:
        if self.is_running or self.report_error_on_close:
          LOGGER.error('Thread %s reports an error:', self.name, exc_info=1)
        self.pause()

  def _on_pause(self):
    super(TimeLoop, self)._on_pause()
    self.pause_time = time.time() - self.start_time

  def _on_run(self):
    super(TimeLoop, self)._on_run()
    t = time.time()
    self.start_time = t - self.pause_time
    self.next_loop_time = self.next_time(t)
    print('!!!! 1', self.start_time - self.load_time,
          self.next_loop_time - self.load_time)
    self.thread = threading.Thread(target=self.target)
    self.thread.daemon = True
    self.thread.start()

  def single_loop(self):
    t = time.time()
    if t >= self.next_loop_time:
      self.loop_target(t)
      self.next_loop_time = self.next_time(self.next_loop_time)
      if self.next_loop_time <= t:
        self.next_loop_time = self.next_time(t)

    if self.is_running:
      sleep_time = min(DEFAULT_TIMEOUT, self.next_loop_time - t)
      if sleep_time > 0:
        time.sleep(sleep_time)
      else:
        LOGGER.error('Sleeping for negative time %s', sleep_time, limit=10)

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

  def next_time(self, t):
    return t + self.time_loop.interval

  def loop_target(self, t):
    pass

  # You can implement Loop.next_time and Loop.loop_target to override the
  # methods in TimeLoop.
