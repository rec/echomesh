"""
>>> split('')
[]

>>> split('x=2')
[[u'x', 2]]

>>> split('x=false')
[[u'x', False]]

>>> split('x="a b c"')
[[u'x', 'a b c']]

>>> do_try('xyz="')
ERROR: At column 5: unterminated quotation mark.

>>> split('x=[1, 2, 3]')
[[u'x', [1, 2, 3]]]

>>> split('x=[1, 2]')
[[u'x', [1, 2]]]

>>> split('x={1: 2, 3: 4}')
[[u'x', {1: 2, 3: 4}]]

>>> split('x=[{1: 2, 3: 4}]')
[[u'x', [{1: 2, 3: 4}]]]

>>> split('light.display.layout=[64, 0]')
[[u'light.display.layout', [64, 0]]]

>>> do_try('x=[{1: 2, 3: 4]}')
ERROR: At column 15: Got closing [ for opening {.

>>> part = 'x=[{1: 2, 3: 4}]'

>>> split(part)
[[u'x', [{1: 2, 3: 4}]]]

>>> do_try(part[:-1])
ERROR: At column 15: missing closing brackets in [.

>>> do_try(part[:-2])
ERROR: At column 14: missing closing brackets in [{.

>>> split('x=2 y=3')
[[u'x', 2], [u'y', 3]]

>>> split('extra= 32')
[[u'extra', 32]]

>>> split('extra =32')
[[u'extra', 32]]

>>> split('extra = 32')
[[u'extra', 32]]

>>> split('ac.de = .defeg.')
[[u'ac.de', '.defeg.']]

>>> split('extra="32 men" ac.de = .defeg. foo = [ bar, baz ]')
[[u'extra', '32 men'], [u'ac.de', '.defeg.'], [u'foo', ['bar', 'baz']]]

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base.Args import *

def do_try(x):
  try:
    split(x)
  except Exception as e:
    print('ERROR:', e)
  else:
    raise Exception('Should have failed')
