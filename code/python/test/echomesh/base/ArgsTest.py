"""
>>> split_args('')
[]

>>> split_args('x=2')
[[[u'x'], u'2']]

>>> split_args('x="a b c"')
[[[u'x'], u'"a b c"']]

>>> do_try('xyz="a')
ERROR: At column 6: unterminated quotation mark.

>>> do_try('xyz')
ERROR: At column 3: expected to see a value.

>>> do_try('xyz=')
ERROR: At column 4: expected to see a value.

>>> split_args('x=[1, 2, 3]')
[[[u'x'], u'[1, 2, 3]']]

>>> split_args('x=[1, 2]')
[[[u'x'], u'[1, 2]']]

>>> split_args('x={1: 2, 3: 4}')
[[[u'x'], u'{1: 2, 3: 4}']]

>>> split_args('x=({1: 2, 3: 4})')
[[[u'x'], u'({1: 2, 3: 4})']]

>>> do_try('x=({1: 2, 3: 4)}')
ERROR: At column 15: Got closing ( for opening {.

>>> part = 'x=({1: 2, 3: 4})'

>>> split_args(part)
[[[u'x'], u'({1: 2, 3: 4})']]

>>> do_try(part[:-1])
ERROR: At column 15: Missing closing brackets for (.

>>> do_try(part[:-2])
ERROR: At column 14: Missing closing brackets for ({.

>>> split_args('x=2 y=3')
[[[u'x'], u'2'], [[u'y'], u'3']]

>>> split_args('extra= 32')
[[[u'extra'], u'32']]

>>> split_args('extra =32')
[[[u'extra'], u'32']]

>>> split_args('extra = 32')
[[[u'extra'], u'32']]

>>> split_args('ac.de = .defeg.')
[[[u'ac', u'de'], u'.defeg.']]

>>> split_args('extra="32 men" ac.de = .defeg. foo = [ bar, baz ]')
[[[u'extra'], u'"32 men"'], [[u'ac', u'de'], u'.defeg.'], [[u'foo'], u'[ bar, baz ]']]

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
