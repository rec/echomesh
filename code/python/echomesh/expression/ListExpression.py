from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression.UnitExpression import UnitExpression
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class ListExpression(object):
  def __init__(self, expression, element):
    self.expressions = []
    self._is_constant = True
    for e in self.expressions:
      expr = UnitExpression(e, element)
      self.expressions.append(expr)
      self._is_constant = self._is_constant and expr.is_constant()

    if self._is_constant:
      self.value = self._evaluate()

  def is_constant(self):
    return self._is_constant

  def evaluate(self):
    return self.value if self._is_constant else self._evaluate()

  def _evaluate(self):
    return [e.evaluate() for e in self.expressions()]
