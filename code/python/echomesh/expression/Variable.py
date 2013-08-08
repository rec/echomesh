
"""
Represent a set of variables in an Element.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import time

from echomesh.expression import Expression
from echomesh.expression import UnitConfig
from echomesh.expression.UnitExpression import UnitExpression
from echomesh.expression import Units
from echomesh.expression.Envelope import Envelope
from echomesh.util import Log
from echomesh.util import Registry
from echomesh.util.math import Interval

LOGGER = Log.logger(__name__)

REGISTRY = Registry.Registry('variable classes')
INFINITY = float('inf')

def variable(description, element):
  if isinstance(description, dict):
    description = copy.copy(description)
    vtype = description.pop('type', None)
    if vtype:
      return REGISTRY.get(vtype)(description, element)
    else:
      raise Exception('No type in variable %s.' % description)
  else:
    return UnitExpression(description, element)

class _Counter(object):
  def __init__(self, element, period, begin=None, end=None, count=None, skip=1,
               repeat=INFINITY, **kwds):
    length = None if count is None else skip * count
    parts = [Expression.convert(x, element) for x in (count, begin, end, skip)]
    self.count, self.begin, self.end, self.skip = Interval.interval(*parts)

    self.element = element
    self.period = Expression.convert(period, element)
    self.repeat = repeat
    if kwds:
      LOGGER.error('Unused keywords %s', kwds)

  def is_constant(self):
    return self.count <= 1

  def evaluate(self):
    if self.is_constant():
      return self.begin

    count = int(UnitConfig.get('speed') * self.element.elapsed_time() //
                self.period)
    if self.count != Units.INFINITY:
      repeat = count // self.count
      if repeat >= self.repeat:
        return self.end
      count -= repeat * self.count
    return self.begin + self.skip * count

def _counter(description, element):
  return _Counter(element, **description)

REGISTRY.register_all(
  counter=_counter,
  envelope=Envelope,
  value=UnitExpression,
  )
