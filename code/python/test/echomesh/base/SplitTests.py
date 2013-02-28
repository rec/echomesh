"""
>>> split_words(', hello, there!')
[u'hello', u'there!']

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

>>> pair_split(split_words('hello as hell, dogs as cats'))
[(u'hello', u'hell'), (u'dogs', u'cats')]

>>> pair_split(split_words('hello,  hell as dogs, cats'))
[(u'hello', u'dogs'), (u'hell', u'cats')]

>>> list(split_args([]))
[]

>>> list(split_args(['extra=32']))
[([u'extra'], u'32')]

>>> list(split_args(['extra=', '32']))
[([u'extra'], u'32')]

>>> list(split_args(['extra', '=32']))
[([u'extra'], u'32')]

>>> list(split_args(['extra', '=', '32']))
[([u'extra'], u'32')]

>>> list(split_args(['ac:', ':de:', '=', ':defeg:']))
[([u'ac', u'de'], u':defeg:')]

>>> list(split_args(['extra=', '32 men', 'ac:', ':de:', '=', ':defeg:']))
[([u'extra'], u'32 men'), ([u'ac', u'de'], u':defeg:')]


>>> split_args_to_dict([])
{}

>>> split_args_to_dict(['extra=32'])
{u'extra': u'32'}

>>> split_args_to_dict(['extra=', '32'])
{u'extra': u'32'}

>>> split_args_to_dict(['extra', '=32'])
{u'extra': u'32'}

>>> split_args_to_dict(['extra', '=', '32'])
{u'extra': u'32'}

>>> split_args_to_dict(['ac:', ':de:', '=', ':defeg:'])
{u'ac': {u'de': u':defeg:'}}

>>> sorted(split_args_to_dict(['extra=', '32 men', 'ac:', ':de:', '=', ':defeg:']).iteritems())
[(u'ac', {u'de': u':defeg:'}), (u'extra', u'32 men')]

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base.Split import *
