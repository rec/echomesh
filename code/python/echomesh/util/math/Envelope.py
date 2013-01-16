from __future__ import absolute_import, division, print_function, unicode_literals

import bisect

class Envelope(object):
  def __init__(self, data, find=bisect.bisect):
    self.find = find
    try:
      self.times, self.data = zip(*data)
      self.length = self.times[-1]
      self.is_constant = False
      self.slot = 0

    except TypeError:
      self.data = data
      self.is_constant = True
      self.length = 0

  def interpolate(self, time):
    # LOG('interpolate', time, self.times)
    if self.is_constant:
      return self.data

    if time <= 0.0:
      return self.data[0]

    if time >= self.length:
      return self.data[-1]

    if time < self.times[self.slot]:
      self.slot = 0

    for self.slot in range(self.slot, len(self.times) - 1):
      t1, t2 = self.times[self.slot:self.slot + 2]
      if t1 <= time <= t2:
        d1, d2 = self.data[self.slot:self.slot + 2]
        ratio = float(time - t1) / (t2 - t1)

        try:
          items = zip(iter(d1), iter(d2))
        except TypeError:
          try:
            return d1 * (1 - ratio) + d2 * ratio
          except:
            print(d1, d2, ratio)
            raise

        return [i1 * (1 - ratio) + i2 * ratio for (i1, i2) in items]

    assert False, "Envelope times are out of order."

def make_envelope(data):
  return data if isinstance(data, Envelope) else Envelope(data)
