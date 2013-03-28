from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import BNF
from echomesh.expression import Evaluator
from echomesh.expression import Values

class Expression(object):
  def __init__(self, expression):
    self.expression = expression
    self.is_variable = True
    self.stack = []

    BNF.bnf(self.stack).parseString(expression, parseAll=True)
    self.value = None

  def evaluate(self, element=None):
    if self.is_variable or self.value is None:
      # TODO: why does this fix our testing bug?

      evaluator = Evaluator.Evaluator(self.stack, Values.Values(element))
      self.value = evaluator.evaluate()
      assert not evaluator.stack

    return self.value

def evaluate(expression, element=None):
  return Expression(expression).evaluate(element)
