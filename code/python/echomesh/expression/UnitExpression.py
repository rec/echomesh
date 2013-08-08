from __future__ import absolute_import, division, print_function, unicode_literals

import re

from echomesh.expression.ReplaceUnicodeFractions import replace_unicode_fractions
from echomesh.expression import Convert
from echomesh.expression import RawExpression
from echomesh.expression import Units

_ANY_UNIT = re.compile(r'( .*? (?: \d\.? | \s | \) ) ) ( [a-z%]* ) \s* $', re.X)

class UnitExpression(object):
  def __init__(self, expression, assume_minutes=True):
    self.expression = self.value = None
    if expression is not None:
      expr = replace_unicode_fractions(expression)
      self.value = Convert.convert_number(expr, assume_minutes)
      if self.value is None:
        expr = expr.lower()
        unit_match = _ANY_UNIT.match(expr)

        if unit_match:
          expr, unit = unit_match.groups()
          self.unit_converter = Units.UNITS.get(unit)
        else:
          self.unit_converter = None

        self.expression = RawExpression.RawExpression(expr)

  def evaluate(self, element=None):
    if not self.expression:
      return self.value

    val = self.expression.evaluate(element)
    if self.unit_converter:
      print('!!!', type(self.unit_converter))
      print('!!!!!', getattr(self.unit_converter, '__name__', None))

      return self.unit_converter(val)
    else:
      return val

  def __call__(self, element=None):
    return self.evaluate(element)

  def is_constant(self, element=None):
    return not self.expression or self.expression.is_constant(element)

def convert(number, element=None, assume_minutes=True):
  if number is None:
    return number
  return UnitExpression(number, assume_minutes).evaluate(element)
