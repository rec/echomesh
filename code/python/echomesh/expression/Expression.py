from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import Envelope
from echomesh.expression import Units

class Expression(object):
  def __init__(self, expression, element=None):
    self.element = element
    if isinstance(expression, dict):
      self.expression = Envelope.Envelope(expression)
    else:
      self.expression = Units.UnitExpression(expression)

  def is_constant(self, element=None):
    return self.expression.is_constant(element or self.element)

  def evaluate(self, element=None):
    return self.expression.evaluate(element or self.element)
