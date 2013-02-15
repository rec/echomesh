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

>>> registry = Registry.Registry('test')
>>> registry.register('foo', 'item1')
>>> registry.register('fot', 'item2')
>>> registry.register('bar', 'item3')
>>> registry.get('foo')
u'item1'

>>> registry.get('b')
u'item3'

>>> registry_exception(registry, 'fo')
Name "fo" matches multiple entries in registry test.

>>> registry.allow_prefixes = False
>>> registry_exception(registry, 'fo')
Didn't find "fo" in registry test.

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
from echomesh.util.UniqueName import unique_name
from echomesh.util import Registry
from echomesh.util.Reserver import Reserver

def registry_exception(registry, name):
  try:
    print(registry.get(name))
  except Exception as e:
    print(e)

