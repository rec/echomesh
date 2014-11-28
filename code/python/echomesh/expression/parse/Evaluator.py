import operator

from echomesh.expression.parse import Values

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

    def pop_and_evaluate(self):
        op = self.stack.pop()

        if op == 'unary -':
            return -self.pop_and_evaluate()

        if op in OPERATORS:
            op2 = self.pop_and_evaluate()
            op1 = self.pop_and_evaluate()
            return OPERATORS[op](op1, op2)

        if op.startswith('0x') or op.startswith('0X'):
            return int(op, 16)

        if op[0].isalpha():
            return Values.evaluate(op, self, self.element)

        if '.' in op or 'e' in op or 'E' in op:
            return float(op)

        return int(op)
