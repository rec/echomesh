from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import BNF
from echomesh.expression import Evaluator
from echomesh.expression import Values

class Expression(object):
  def __init__(self, expression):
    self.expression = expression
    self._is_variable = None
    self.stack = []

    BNF.bnf(self.stack).parseString(expression, parseAll=True)
    self.value = None

  def is_variable(self, element=None):
    if self._is_variable is None:
      self._is_variable = any((s[0].isalpha() and
                               Values.is_variable(s, element))
                              for s in self.stack)
    return self._is_variable

  def evaluate(self, element=None):
    if self.is_variable or self.value is None:
      evaluator = Evaluator.Evaluator(self.stack, element)
      self.value = evaluator.evaluate()
      assert not evaluator.stack

    return self.value

def evaluate(expression, element=None):
  return Expression(expression).evaluate(element)
