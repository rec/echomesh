from __future__ import absolute_import, division, print_function, unicode_literals

import re

from echomesh.expression.ReplaceUnicodeFractions import replace_unicode_fractions
from echomesh.expression import Convert
from echomesh.expression import RawExpression
from echomesh.expression import Units

_ANY_UNIT = re.compile(r'( .*? (?: \d\.? | \s | \) ) ) ( [a-z%]* ) \s* $', re.X)

class UnitExpression(object):
  def __init__(self, expression, element=None, assume_minutes=True):
    self.element = element
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

        self.expression = RawExpression.RawExpression(expr, element)

  def evaluate(self):
    if not self.expression:
      return self.value

    val = self.expression.evaluate()
    if self.unit_converter:

      return self.unit_converter(val)
    else:
      return val

  def is_constant(self):
    return not self.expression or self.expression.is_constant()

