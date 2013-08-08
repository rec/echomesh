import operator

from echomesh.expression import Values

OPERATORS = {
  '+': operator.add,
  '-': operator.sub,
  '*': operator.mul,
  '/': operator.truediv,
  '**': operator.pow,
  }

class Evaluator(object):
  def __init__(self, stack, element):
    self.stack = stack[:]
    self.element = element

  def evaluate(self):
    op = self.stack.pop()

    if op == 'unary -':
      return -self.evaluate()

    if op in OPERATORS:
      op2 = self.evaluate()
      op1 = self.evaluate()
      return OPERATORS[op](op1, op2)

    if op.startswith('0x') or op.startswith('0X'):
      return int(op, 16)

    if op[0].isalpha():
      return Values.evaluate(op, self, self.element)

    if '.' in op or 'e' in op or 'E' in op:
      return float(op)

    return int(op)
