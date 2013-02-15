"""
>>> Join.join_words()
u''

>>> Join.join_words('hello')
u'hello'

>>> Join.join_words('hello', 'goodbye')
u'hello and goodbye'

>>> Join.join_words('apples', 'oranges', 'pears')
u'apples, oranges, and pears'
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Join
