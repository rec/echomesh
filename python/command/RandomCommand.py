from __future__ import absolute_import, division, print_function, unicode_literals

import time

from util import Poisson
from util.ThreadLoop import ThreadLoop

DEFAULT_TIMEOUT = 0.5
DEFAULT_INTERVAL = 10.0

class RandomCommand(ThreadLoop):
  def __init__(self, score, rule, timeout=DEFAULT_TIMEOUT):
    ThreadLoop.__init__(self)
    self.score = score
    self.rule = rule
    self.mean = rule.get('data', {}).get('mean', DEFAULT_INTERVAL)
    keys = list(rule.get('mapping', {}).iterkeys())
    self.key = keys[0] if keys else 'none'
    self._next_event(time.time())

  def _next_event(self, t):
    self.time = t + Poisson.next_poisson(self.mean)

  def run(self):
    t = time.time()
    if t >= self.time:
      self.score.execute_rule(self.rule, self.key)
      self._next_event(t)
    time.sleep(min(DEFAULT_TIMEOUT, self.time - t))
