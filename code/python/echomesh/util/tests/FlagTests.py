"""
>>> Flag.split_flag('')
(u'', u'')

>>> Flag.split_flag('-')
(u'', u'')

>>> Flag.split_flag('-x')
(u'x', u'')

>>> Flag.split_flag('--hello')
(u'hello', u'')

>>> Flag.split_flag('--hello=')
(u'hello', u'')

>>> Flag.split_flag('--hello=world')
(u'hello', u'world')

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Flag
