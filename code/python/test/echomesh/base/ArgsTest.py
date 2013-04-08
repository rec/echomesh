"""
>>> split_args([])
[]

>>> split_args(['extra=32'])
[[[u'extra'], u'32']]

>>> split_args(['extra=', '32'])
[[[u'extra'], u'32']]

>>> split_args(['extra', '=32'])
[[[u'extra'], u'32']]

>>> split_args(['extra', '=', '32'])
[[[u'extra'], u'32']]

>>> split_args(['ac.', 'de.', '=', '.defeg.'])
[[[u'ac', u'de'], u'.defeg.']]

>>> split_args(['extra=', '32 men', 'ac', '.de.', '=', '.defeg.'])
[[[u'extra'], u'32 men'], [[u'ac', u'de'], u'.defeg.']]

>>> split_args2('')
[]

>>> split_args2('x=2')
[[[u'x'], u'2']]

>>> split_args2('x=2 y=3', not True)
[[[u'x'], u'2'], [[u'y'], u'3']]

>>> split_args2('extra= 32')
[[[u'extra'], u'32']]

>>> split_args2('extra =32')
[[[u'extra'], u'32']]

>>> split_args2('extra = 32')
[[[u'extra'], u'32']]

>>> split_args2('ac.de = .defeg.')
[[[u'ac', u'de'], u'.defeg.']]

>>> split_args2('extra="32 men" ac.de = .defeg. foo = [ bar, baz ]')
[[[u'extra'], u'"32 men"'], [[u'ac', u'de'], u'.defeg.'], [[u'foo'], u'[ bar, baz ]']]

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base.Args import *
