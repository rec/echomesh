"""
>>> evaluate('2+2')
4

>>> evaluate('2+sin(0)')
2.0

>>> evaluate('2 + trunc(1.2)')
3

>>> evaluate('-cos(0)')
-1.0

>>> evaluate_fail('2 +')
EXCEPTION: Expected end of text (at char 2), (line:1, col:3)

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.math.Expressions import evaluate

def evaluate_fail(expr):
  try:
    evaluate(expr)
    print('ERROR: %s evaluated OK!' % expr)
  except Exception as e:
    print('EXCEPTION:', e)

