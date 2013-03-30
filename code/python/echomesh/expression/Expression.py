from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import Envelope
from echomesh.expression import Units

class Expression(object):
  def __init__(self, expression, element=None):
    self.element = element
    if isinstance(expression, dict):
      self.envelope = Envelope.Envelope(expression)
      self.unit_expression = None
    else:
      self.envelope = None
      self.unit_expression = Units.UnitExpression(expression)

  def __call__(self, element=None):
    element = element or self.element
    if self.envelope:
      return self.envelope.interpolate(element.time)
    else:
      return self.unit_expression(element)

  def evaluate(self, element=None):
    # TODO: get rid of __call__
    return self(element)

  def is_variable(self, element=None):
    if self.envelope:
      return self.envelope.is_variable
    else:
      return self.unit_expression.is_variable(element)

