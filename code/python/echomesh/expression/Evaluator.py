import operator

OPERATORS = {
  '+': operator.add,
  '-': operator.sub,
  '*': operator.mul,
  '/': operator.truediv,
  '**': operator.pow,
  }

class Evaluator(object):
  def __init__(self, stack, variables):
    self.stack = stack[:]
    self.variables = variables

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
      return self.variables.evaluate(op, self)

    if '.' in op or 'e' in op or 'E' in op:
      return float(op)

    return int(op)


"""
Three different types of things, three delimiters:

* functions of 1 variable (sin, cos, etc) - nothing or function
* config - config.
* system values (pi, e, time, date) - sys.
* element values: element.

"""
