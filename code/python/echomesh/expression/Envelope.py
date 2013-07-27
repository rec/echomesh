from __future__ import absolute_import, division, print_function, unicode_literals

import bisect

from echomesh.expression import SplitNumbers
from echomesh.expression import Units
from echomesh.util import Dict
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Envelope(object):
  _FIELDS = 'data', 'length', 'loops', 'reverse', 'times'

  def __init__(self, data):
    self.is_constant = not isinstance(data, dict)
    if self.is_constant:
      self.data = Units.convert(data)
      self.length = 0
      return

    kwds, numeric = SplitNumbers.split(data)
    self.times, self.data = zip(*numeric)
    if not data:
      raise Exception('Didn\'t understand envelope %s' % data)

    if len(self.data) == 1:
      self.is_constant = True
      self.data = Units.convert(data[0])
      self.length = 0
      return

    for i in range(1, len(self.times)):
      if self.times[i - 1] >= self.times[i]:
        raise Exception('Envelope times must be strictly increasing.')

    for i, t in enumerate(self.times):
      if t < 0:
        raise Exception('Envelope times cannot be negative.')

    self.loops = kwds.get('loops', 1)
    self.reverse = kwds.get('reverse', False)
    self.loop_length = self.times[-1]

    length = kwds.get('length')
    if length:
      self.length = Units.convert(length)
      if self.length < 0:
        LOGGER.error('Negative length "%s" is not allowed.', length)
        self.length = 0
    else:
      self.length = self.loop_length * self.loops

    if self.length:
      self.slot = 0
    else:
      self.is_constant = True
      self.data = Units.convert(self.data[0])

  def description(self):
    return Dict.from_attributes(self, Envelope._FIELDS)

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
