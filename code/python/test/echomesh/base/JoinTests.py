"""
>>> join_words([])
u''

>>> join_words(['hello'])
u'hello'

>>> join_words(['hello', 'goodbye'])
u'goodbye and hello'

>>> join_words(['apples', 'oranges', 'pears'])
u'apples, oranges, and pears'
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base.Join import *
