from pyparsing import Literal, CaselessLiteral, Word, Group, Optional, \
  ZeroOrMore, Forward, nums, alphas, Regex, ParseException

import math
import operator
import re

def bnf(exprStack):
  """
  expop   :: '^'
  multop  :: '*' | '/'
  addop   :: '+' | '-'
  integer :: ['+' | '-'] '0'..'9'+
  atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
  factor  :: atom [ expop factor ]*
  term    :: factor [ multop factor ]*
  expr    :: term [ addop term ]*
  """
  def pushFirst(strg, loc, toks):
    exprStack.append(toks[0])

  def pushUMinus(strg, loc, toks):
    for t in toks:
      if t == '-':
        exprStack.append('unary -')
      else:
        break

  point = Literal('.')
  e = CaselessLiteral('E')
  fnumber = Regex(r' [+-]? \d+ (:? \. \d* )? (:? [eE] [+-]? \d+)?', re.X)
  xnumber = Regex(r'0 [xX] [0-9 a-f A-F]+', re.X)
  ident = Word(alphas, alphas+nums+'_$.')

  plus  = Literal('+')
  minus = Literal('-')
  mult  = Literal('*')
  div   = Literal('/')

  lpar  = Literal('(').suppress()
  rpar  = Literal(')').suppress()
  addop  = plus | minus
  multop = mult | div
  expop = Literal('**')
  pi    = CaselessLiteral('PI')

  expr = Forward()
  atom_parts = pi | e | fnumber | xnumber | ident + lpar + expr + rpar | ident
  atom_action = atom_parts.setParseAction(pushFirst)
  group = Group(lpar + expr + rpar)
  atom = ((0, None) * minus + atom_action | group).setParseAction(pushUMinus)

  # by defining exponentiation as 'atom [ ^ factor ]...'
  # instead of 'atom [ ^ atom ]...', we get right-to-left exponents, instead of left-to-righ
  # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
  factor = Forward()
  factor << atom + ZeroOrMore((expop + factor).setParseAction(pushFirst))

  term = factor + ZeroOrMore((multop + factor).setParseAction(pushFirst))
  expr << term + ZeroOrMore((addop + term).setParseAction(pushFirst))

  return expr

# map operator symbols to corresponding arithmetic operations
EPSILON = 1e-12
OPERATORS = {
  '+': operator.add,
  '-': operator.sub,
  '*': operator.mul,
  '/': operator.truediv,
  '**': operator.pow,
  }

class Evaluator(object):
  def __init__(self, stack, variables, functions):
    self.stack = stack[:]
    self.variables = variables
    self.function = functions

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

    if op.startswith('$'):
      return self.functions[op[1:]](self.evaluate())

    if op[0].isalpha():
      return self.variables.evaluate(op)

    if '.' in op or 'e' in op or 'E' in op:
      return float(op)

    return int(op)

FUNCTIONS = {
  'sin': math.sin,
  'cos': math.cos,
  'tan': math.tan,
  'abs': abs,
  'trunc': lambda a: int(a),
  'round': round,
  'sgn': lambda a: abs(a) > EPSILON and cmp(a,0) or 0
  }

class Expression(object):
  def __init__(self, expression, variables=None, functions=FUNCTIONS):
    self.expression = expression
    self.variables = variables
    self.functions = functions
    self.is_variable = True
    self.stack = []
    bnf(self.stack).parseString(expression, parseAll=True)
    self.value = None

  def evaluate(self):
    if self.is_variable or self.value is None:
      evaluator = Evaluator(self.stack, self.variables,
                            self.functions)
      self.value = evaluator.evaluate()
      assert not evaluator.stack

    return self.value


def evaluate(expression, variables=None):
  return Expression(expression, variables).evaluate()

from pyparsing import ParserElement

ParserElement.verbose_stacktrace = True


"""
Three different types of things, three delimiters:

* functions of 1 variable (sin, cos, etc) - nothing or function
* config - config.
* system values (pi, e, time, date) - sys.
* element values: element.

"""
