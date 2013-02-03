from __future__ import absolute_import, division, print_function, unicode_literals

import bisect
from python import six

from echomesh.util.math import Units

class Envelope(object):
  def __init__(self, data, find=bisect.bisect):
    self.find = find

    iterator = None
    if not isinstance(data, six.string_types):
      try:
        iterator = data.iteritems()
      except AttributeError:
        try:
          iterator = iter(data)
        except TypeError:
          pass

    if iterator:
      self.times, self.data = zip(*sorted(iterator))
      self.times = [Units.convert(t) for t in self.times]
      self.length = self.times[-1]
      self.is_constant = False
      self.slot = 0
    else:
      self.data = [data]
      self.is_constant = True
      self.length = 0

    self.data = [Units.convert(d) for d in self.data]

  def interpolate(self, time):
    if self.is_constant or time <= 0.0:
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
