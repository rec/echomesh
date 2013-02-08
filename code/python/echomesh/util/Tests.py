"""

>>> unique_name('', [])
u''

>>> unique_name('foo', ['bar', 'baz'])
u'foo'

>>> unique_name('bar', ['bar', 'baz'])
u'bar.1'

>>> unique_name('bar', ['bar', 'baz', 'bar.1',])
u'bar.2'

>>> unique_name('bar.1', ['bar', 'baz', 'bar.1',])
u'bar.2'

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.UniqueName import unique_name
