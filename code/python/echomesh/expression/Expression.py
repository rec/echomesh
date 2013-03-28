from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import Envelope
from echomesh.expression import Units

class Expression(object):
  def __init__(self, expression):
    if isinstance(expression, dict):
      self.envelope = Envelope.Envelope(expression)
      self.unit_expression = None
    else:
      self.envelope = None
      self.unit_expression = Units.UnitExpression(expression)

  def __call__(self, element=None):
    if self.envelope:
      return self.envelope.interpolate(element.time)
    else:
      return self.unit_expression.evaluate(element)