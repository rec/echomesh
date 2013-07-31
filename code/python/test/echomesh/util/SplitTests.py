"""
>>> split_words('hello, there!')
[u'hello,', u'there!']

>>> split_words('')
[]

>>> split_words('one')
[u'one']

>>> split_words('one two')
[u'one', u'two']

>>> split_words(' one two')
[u'one', u'two']

>>> split_words('one two')
[u'one', u'two']

>>> split_words(' one two ')
[u'one', u'two']

>>> pair_split([])
[]

>>> pair_split(split_words('hello'))
[(u'hello', None)]

>>> pair_split(split_words('hello as hell'))
[(u'hello', u'hell')]

>>> pair_split(split_words('hello as hell dogs as cats'))
[(u'hello', u'hell'), (u'dogs', u'cats')]

>>> pair_split(split_words('hello  hell as dogs cats'))
[(u'hello', u'dogs'), (u'hell', u'cats')]

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.string.Split import *
