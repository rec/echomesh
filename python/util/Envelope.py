from __future__ import absolute_import, division, print_function, unicode_literals

import bisect

class Envelope(object):
  def __init__(self, data):
    try:
      self.times, self.data = zip(*data)
      self.last = len(self.data) - 1
      self.is_constant = False
    except TypeError:
      self.data = data
      self.is_constant = True

  def interpolate(self, time):
    if self.is_constant:
      return self.data
    index = bisect.bisect(self.times, time)
    if index is 0:
      return self.data[0]
    if index > self.last:
      return self.data[self.last]

    t1, d1 = self.times[index - 1], self.data[index - 1]
    if time <= t1:
      # print('here!', time, t1)
      return d1

    t2, d2 = self.times[index], self.data[index]
    if time >= t2:
      return d2

    ratio = float(time - t1) / (t2 - t1)

    try:
      items = zip(iter(d1), iter(d2))
    except TypeError:
      return d1 * (1 - ratio) + d2 * ratio

    return [i1 * (1 - ratio) + i2 * ratio for (i1, i2) in items]

def make_envelope(data):
  return data if isinstance(data, Envelope) else Envelope(data)
