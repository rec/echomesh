from __future__ import absolute_import, division, print_function, unicode_literals

import bisect

from echomesh.util.math import Units
from echomesh.util.math import SplitNumbers

USE_BISECT = False

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

    if USE_BISECT:
      pass

    if time < self.times[self.slot]:
      self.slot = 0

    for self.slot in range(self.slot, len(self.times) - 1):
      t1, t2 = self.times[self.slot:self.slot + 2]
      if t1 <= time <= t2:
        break
    else:
      assert False, "Envelope times are out of order."

    d1, d2 = self.data[self.slot:self.slot + 2]
    ratio = float(time - t1) / (t2 - t1)

    try:
      items = zip(iter(d1), iter(d2))
    except TypeError:
      return d1 * (1 - ratio) + d2 * ratio

    return [i1 * (1 - ratio) + i2 * ratio for (i1, i2) in items]


def make_envelope(data):
  return data if isinstance(data, Envelope) else Envelope(data)
