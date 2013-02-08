"""
>>> test_parse('9')
9

>>> test_parse('-9')
-9

>>> test_parse('--9')
9

>>> test_parse('-E')
-2.718281828459045

>>> test_parse('9 + 3 + 6')
18

>>> test_parse('9 + 3 / 11')
9.272727272727273

>>> test_parse('(9 + 3)')
12

>>> test_parse('(9+3) / 11')
1.0909090909090908

>>> test_parse('9 - 12 - 6')
-9

>>> test_parse('9 - (12 - 6)')
3

>>> test_parse('2*3.14159')
6.28318

>>> test_parse('3.1415926535*3.1415926535 / 10')
0.9869604400525172

>>> test_parse('PI * PI / 10')
0.9869604401089358

>>> test_parse('PI*PI/10')
0.9869604401089358

>>> test_parse('PI^2')
9.869604401089358

>>> test_parse('round(PI^2)')
10.0

>>> test_parse('6.02E23 * 8.048')
4.844896e+24

>>> test_parse('e / 3')
0.9060939428196817

>>> test_parse('sin(PI/2)')
1.0

>>> test_parse('trunc(E)')
2

>>> test_parse('trunc(-E)')
-2

>>> test_parse('round(E)')
3.0

>>> test_parse('round(-E)')
-3.0

>>> test_parse('E^PI')
23.140692632779263

>>> test_parse('2^3^2')
512

>>> test_parse('2^3+2')
10

>>> test_parse('2^3+5')
13

>>> test_parse('2^9')
512

>>> test_parse('sgn(-2)')
-1

>>> test_parse('sgn(0)')
0

>>> test_parse('foo(0.1)')
u'failed eval: invalid identifier "foo"'

>>> test_parse('sgn(0.1)')
1

# >>> test_parse('0x01')
# 1
#
# >>> test_parse('0xff')  # Doesn't yet work.
# 255

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from pyparsing import Expressions
from pyparsing.pyparsing import ParseException

def test_parse(s):
  try:
    return Expressions.evaluate(s)
  except ParseException as pe:
    return 'failed parse: ' + str(pe)
  except Exception as e:
    return 'failed eval: ' + str(e)
