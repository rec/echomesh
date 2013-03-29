
"""
Represent a set of variables in an Element.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import time

from echomesh.expression.Envelope import Envelope
from echomesh.expression import Units
from echomesh.util.math import Interval
from echomesh.util import Registry
from echomesh.util import Log

LOGGER = Log.logger(__name__)

REGISTRY = Registry.Registry('variable classes')
INFINITY = float('inf')

def variable(element, description):
  description = copy.copy(description)
  vtype = description.pop('type', None)
  if vtype:
    return REGISTRY.get(vtype)(element, description)

  raise Exception('No type in variable %s.' % description)

class _Counter(object):
  def __init__(self, element, period, begin=None, end=None, count=None, skip=1,
               repeat=INFINITY, **kwds):
    length = None if count is None else skip * count
    parts = [Units.convert(x, element) for x in (count, begin, end, skip)]
    self.count, self.begin, self.end, self.skip = Interval.interval(*parts)

    self.element = element
    self.period = Units.convert(period, element)
    self.repeat = repeat
    if kwds:
      LOGGER.error('Unused keywords %s', kwds)

  def is_variable(self):
    return self.count > 1

  def evaluate(self):
    if not self.is_variable():
      return self.begin

    count = int(self.element.elapsed_time() // self.period)
    repeat = count // self.count
    if repeat >= self.repeat:
      return self.end
    count -= repeat * self.count
    return self.begin + self.skip * count

def _counter(element, description):
  return _Counter(element, **description)

class _Envelope(Envelope):
  def __init__(self, element, kwds):
    self.element = element
    super(_Envelope, self).__init__(kwds)

  def evaluate(self):
    return self.interpolate(self.element.elapsed_time())

REGISTRY.register_all(
  counter=_counter,
  envelope=_Envelope,
  )
