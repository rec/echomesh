from __future__ import absolute_import, division, print_function, unicode_literals

import bisect

from echomesh.expression import Units
from echomesh.util.math import SplitNumbers

class Envelope(object):
  def __init__(self, data):
    self.is_constant = not isinstance(data, dict)
    if self.is_constant:
      self.data = Units.convert(data)
      self.length = 0

    else:
      kwds, numeric = SplitNumbers.split(data)
      self.times, self.data = zip(*numeric)

      self.loops = kwds.get('loops', 1)
      self.reverse = kwds.get('reverse', False)
      self.loop_length = self.times[-1]

      length = kwds.get('length')
      if length:
        self.length = Units.convert(length)
      else:
        self.length = self.loop_length * self.loops
      self.slot = 0

  def interpolate(self, time):
    if self.is_constant:
      return self.data
    elif time <= 0.0:
      return self.data[0]
    elif time >= self.length:
      return self.data[-1]

    loop_count = int(time / self.loop_length)
    time %= self.loop_length
    if self.reverse and (loop_count % 2):
      time = self.loop_length - time

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


def make_envelope(data):
  return data if isinstance(data, Envelope) else Envelope(data)
