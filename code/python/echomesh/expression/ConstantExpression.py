from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression.UnitExpression import UnitExpression

def constant_expression(expr):
  ue = UnitExpression(None)
  ue.value = expr
  return ue
