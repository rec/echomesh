"""
>>> Flag.split_flag('')
(u'', True)

>>> Flag.split_flag('-')
(u'', True)

>>> Flag.split_flag('-x')
(u'x', True)

>>> Flag.split_flag('--hello')
(u'hello', True)

>>> Flag.split_flag('--hello=')
(u'hello', True)

>>> Flag.split_flag('--hello=world')
(u'hello', u'world')

>>> Flag.split_args(['hello', '--foo', '--bar=baz', '--bing', 'world'])
({u'bing': True, u'foo': True, u'bar': u'baz'}, [u'hello', u'world'])

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Flag
