"""
Represent a set of variables in an Element.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.expression import Expression
from echomesh.expression import UnitSettings
from echomesh.expression.UnitExpression import UnitExpression
from echomesh.expression.Envelope import Envelope
from echomesh.util import Log
from echomesh.util.registry import Registry
from echomesh.util.math import Interval

LOGGER = Log.logger(__name__)

REGISTRY = Registry.Registry('variable classes')
INFINITY = float('inf')

class _Counter(object):
    def __init__(self, element, period, begin=None, end=None, count=None,
                 skip=1, repeat=INFINITY, **kwds): 
        parts = [
            Expression.convert(x, element) for x in (count, begin, end, skip)]
        self.count, self.begin, self.end, self.skip = Interval.interval(*parts)

        self.element = element
        self.period = Expression.convert(period, element)
        self.repeat = repeat
        if kwds:
            LOGGER.error('Unknown keywords "%s" for counter', kwds)

    def is_constant(self):
        return self.count <= 1

    def evaluate(self):
        if self.is_constant():
            return self.begin

        count = int(UnitSettings.get('speed') * self.element.elapsed_time() //
                    self.period)
        if self.count != INFINITY:
            repeat = count // self.count
            if repeat >= self.repeat:
                return self.end
            count -= repeat * self.count
        value = self.begin + self.skip * count
        return value

def _counter(description, element):
    return _Counter(element, **description)

REGISTRY.register_all(
  counter=_counter,
  envelope=Envelope,
  value=UnitExpression,
  )

def variable(description, element):
    if not isinstance(description, dict):
        return UnitExpression(description, element)

    description = copy.copy(description)
    vtype = description.pop('type', None)
    if not vtype:
        raise Exception('No type in variable, description="%s".' % description)
    return REGISTRY.function(vtype)(description, element)
