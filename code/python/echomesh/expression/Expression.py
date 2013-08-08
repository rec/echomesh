from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import Envelope
from echomesh.expression import Units
from echomesh.expression.UnitExpression import UnitExpression

class Expression(object):
  def __init__(self, expression, element=None):
    self.element = element
    if isinstance(expression, dict):
      self.expression = Envelope.Envelope(expression, element)
    else:
      self.expression = UnitExpression(expression, element)

  def is_constant(self, element=None):
    return self.expression.is_constant(element or self.element)

  def evaluate(self, element=None):
    return self.expression.evaluate(element or self.element)

expression = Expression

def convert(number, element=None, assume_minutes=True):
  if number is None:
    return number
  return UnitExpression(number, assume_minutes, element).evaluate()
