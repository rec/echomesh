"""
>>> split_args('')
[]

>>> split_args('x=2')
[[[u'x'], 2]]

>>> split_args('x="a b c"')
[[[u'x'], 'a b c']]

>>> do_try('xyz="a')
ERROR: At column 6: unterminated quotation mark.

>>> do_try('xyz')
ERROR: At column 3: expected to see a value.

>>> do_try('xyz=')
ERROR: At column 4: expected to see a value.

>>> split_args('x=[1, 2, 3]')
[[[u'x'], [1, 2, 3]]]

>>> split_args('x=[1, 2]')
[[[u'x'], [1, 2]]]

>>> split_args('x={1: 2, 3: 4}')
[[[u'x'], {1: 2, 3: 4}]]

>>> split_args('x=[{1: 2, 3: 4}]')
[[[u'x'], [{1: 2, 3: 4}]]]

>>> split_args('light.display.layout=[64, 0]')
[[[u'light', u'display', u'layout'], [64, 0]]]

>>> do_try('x=[{1: 2, 3: 4]}')
ERROR: At column 15: Got closing [ for opening {.

>>> part = 'x=[{1: 2, 3: 4}]'

>>> split_args(part)
[[[u'x'], [{1: 2, 3: 4}]]]

>>> do_try(part[:-1])
ERROR: At column 15: Missing closing brackets for [.

>>> do_try(part[:-2])
ERROR: At column 14: Missing closing brackets for [{.

>>> split_args('x=2 y=3')
[[[u'x'], 2], [[u'y'], 3]]

>>> split_args('extra= 32')
[[[u'extra'], 32]]

>>> split_args('extra =32')
[[[u'extra'], 32]]

>>> split_args('extra = 32')
[[[u'extra'], 32]]

>>> split_args('ac.de = .defeg.')
[[[u'ac', u'de'], '.defeg.']]

>>> split_args('extra="32 men" ac.de = .defeg. foo = [ bar, baz ]')
[[[u'extra'], '32 men'], [[u'ac', u'de'], '.defeg.'], [[u'foo'], ['bar', 'baz']]]

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base.Args import *

def do_try(x):
  try:
    split_args(x)
  except Exception as e:
    print('ERROR:', e)
  else:
    raise Exception('Should have failed')
