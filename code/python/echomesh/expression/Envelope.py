from __future__ import absolute_import, division, print_function, unicode_literals

import bisect

from echomesh.expression import SplitNumbers
from echomesh.util import Dict
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Envelope(object):
  _FIELDS = 'data', 'length', 'loops', 'reverse', 'times'

  def __init__(self, data, element=None):
    self.element = element

    kwds, numeric = SplitNumbers.split(data)
    self.times, self.data = zip(*numeric)
    if not self.times:
      raise Exception('Didn\'t understand envelope %s' % data)

    if len(self.times) == 1:
      return self._set_constant(self.data[0])

    _check_times(self.times)

    self.loops = kwds.get('loops', 1)
    self.last_time = self.times[-1]

    from echomesh.expression import Expression
    length = kwds.get('length', self.last_time * self.loops)
    self.length = Expression.convert(length, self.element)

    if self.length > 0:
      self._is_constant = False
      self.slot = 0
      self.reverse = kwds.get('reverse', False)

    else:
      self._set_constant(self.data[0])
      if self.length < 0:
        LOGGER.error('Negative length "%s" is not allowed.', length)
        self.length = 0

  def evaluate(self):
    return self.interpolate(self.element.time)

  def is_constant(self):
    return self._is_constant

  def description(self):
    return Dict.from_attributes(self, Envelope._FIELDS)

  def _set_constant(self, value):
    self._is_constant = True
    self.value = Expression.convert(value, self.element)
    self.length = 0

  def interpolate(self, time):
    if self._is_constant:
      return self.data

    elif time <= 0.0:
      return self.data[0]

    elif time >= self.length:
      return self.data[-1]

    loop_count = int(time / self.last_time)
    time %= self.last_time
    if self.reverse and (loop_count % 2):
      time = self.last_time - time

    self.slot = max(bisect.bisect(self.times, time) - 1, 0)
    t1, t2 = self.times[self.slot:self.slot + 2]
    d1, d2 = self.data[self.slot:self.slot + 2]
    ratio = float(time - t1) / (t2 - t1)

    try:
      items = zip(iter(d1), iter(d2))
    except TypeError:
      return d1 * (1 - ratio) + d2 * ratio
    else:
      return [i1 * (1 - ratio) + i2 * ratio for (i1, i2) in items]


def _check_times(times):
  for i in range(1, len(times)):
    if times[i - 1] >= times[i]:
      raise Exception('Envelope times must be strictly increasing.')

  for i, t in enumerate(times):
    if t < 0:
      raise Exception('Envelope times cannot be negative.')

