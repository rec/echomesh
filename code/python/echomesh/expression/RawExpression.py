from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import BNF
from echomesh.expression import Evaluator
from echomesh.expression import Values

class RawExpression(object):
  def __init__(self, expression, element):
    self.element = element
    self.stack = []
    self._is_constant = None

    BNF.bnf(self.stack).parseString(expression, parseAll=True)
    self.value = None

  def is_constant(self, element=None):
    if self._is_constant is None:
      def const(s):
        return not s[0].isalpha() or Values.is_constant(s, element or self.element)
      self._is_constant = all(const(s) for s in self.stack)
    return self._is_constant

  def evaluate(self, element=None):
    element = element or self.element
    if self.value is None or not self.is_constant(element):
      evaluator = Evaluator.Evaluator(self.stack, element)
      self.value = evaluator.evaluate()
      assert not evaluator.stack

    return self.value
