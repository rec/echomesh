"""
>>> Split.split_words(', hello, there!')
[u'hello', u'there!']

>>> Split.split_words('')
[]

>>> Split.split_words('one')
[u'one']

>>> Split.split_words('one two')
[u'one', u'two']

>>> Split.split_words(' one two')
[u'one', u'two']

>>> Split.split_words('one two')
[u'one', u'two']

>>> Split.split_words(' one two ')
[u'one', u'two']

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Split
