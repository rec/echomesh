"""
>>> String.join_words([])
u''

>>> String.join_words(['hello'])
u'hello'

>>> String.join_words(['hello', 'goodbye'])
u'goodbye and hello'

>>> String.join_words(['apples', 'oranges', 'pears'])
u'apples, oranges, and pears'
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import String
