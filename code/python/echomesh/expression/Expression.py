from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.expression.Envelope import Envelope
from echomesh.expression.ListExpression import ListExpression
from echomesh.expression.UnitExpression import UnitExpression

def expression(expr, element):
  try:
    if isinstance(expr, dict):
      return Envelope(expr, element)

    if isinstance(expr, (list, tuple)):
      return ListExpression(expr, element)

    if isinstance(expr, six.string_types) and ',' in expr:
      return ListExpression(expr.split(','), element)

    return UnitExpression(expr, element)
  except:
    raise Exception("Couldn't evaluate expression %s" % expr)

def constant_expression(expr):
  ue = UnitExpression(None)
  ue.value = expr
  return ue

def convert(number, element=None, assume_minutes=True):
  if number is None:
    return number
  return UnitExpression(number, element, assume_minutes).evaluate()
