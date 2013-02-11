"""

>>> res = Reserver()

>>> res.reserved()
[]

>>> res.reserve(1, 2, 3)
>>> set(res.reserved())
set([1, 2, 3])

>>> res.reserve(1, 2, 3)
>>> set(res.reserved())
set([1, 2, 3])

>>> res.unreserve(1, 2)
>>> set(res.reserved())
set([1, 2, 3])

>>> res.unreserve(1)
>>> set(res.reserved())
set([2, 3])

>>> res.unreserve(2, 3)
>>> set(res.reserved())
set([3])

>>> res.unreserve(3)
>>> set(res.reserved())
set([])

>>> res.reserve_uniquely(1, 2)
>>> set(res.reserved())
set([1, 2])

>>> res.reserve_uniquely(1, 2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "echomesh/util/Reserver.py", line 41, in reserve_uniquely
    raise Exception('%s are already reserved.' % res)
Exception: [1, 2] are already reserved.

>>> res.reserve(1, 2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "echomesh/util/Reserver.py", line 32, in reserve
    raise Exception('%s are already uniquely reserved.' % res)
Exception: set([1, 2]) are already uniquely reserved.

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
from echomesh.util.Reserver import Reserver
