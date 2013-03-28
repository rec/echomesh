"""
>>> evaluate('2+2')
4

>>> evaluate('2*2+2')
6

>>> evaluate('2*(2+2)')
8

>>> evaluate('(2*((((2)+2))))')
8

>>> evaluate('2+sin(0)')
2.0

>>> evaluate('2 + trunc(1.2)')
3

>>> evaluate('-cos(0)')
-1.0

>>> evaluate_fail('2 +')
EXCEPTION: Expected end of text (at char 2), (line:1, col:3)

>>> evaluate('3 + sys.pi')
6.141592653589793

>>> evaluate('2 ** 3 ** 2')
512

>>> evaluate('(2 ** 3) ** 2')
64

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import RawExpression

def evaluate(expression):
  return RawExpression.RawExpression(expression).evaluate()

def evaluate_fail(expr):
  try:
    evaluate(expr)
    print('ERROR: %s evaluated OK!' % expr)
  except Exception as e:
    print('EXCEPTION:', e)

def variable_evaluator(x):
  if x == 'x':
    return 1

  if x == 'y':
    return 2

  if x == 'dotted.pair':
    return 7
