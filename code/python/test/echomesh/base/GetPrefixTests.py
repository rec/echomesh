"""
>>> table = {'one': 1, 'two': 2, 'three': 3}
>>> get_prefix(table, 'one')
(u'one', 1)

>>> get_prefix(table, 'o')
(u'one', 1)

>>> get_prefix(table, 'one', allow_prefixes=False)
(u'one', 1)

>>> do_try(get_prefix, table, 'o', allow_prefixes=False)
ERROR: "o" is not valid.

>>> do_try(get_prefix, table, 'x')
ERROR: "x" is not valid.

>>> do_try(get_prefix, table, 't')
ERROR: "t" matches more than one: three and two.

>>> master = {'foo': {'bar': {'baz': 23}}, 'new': {}}
>>> slave = {}

>>> set_assignment('foo.bar.baz', 32, master, slave)
>>> slave
{u'foo': {u'bar': {u'baz': 32}}}

>>> set_assignment('f.b.b', 19, master, slave)
>>> slave
{u'foo': {u'bar': {u'baz': 19}}}

>>> set_assignment('new.foo', 23, master, slave, unmapped_names=set(['new']))
>>> slave
{u'new': {u'foo': 23}, u'foo': {u'bar': {u'baz': 19}}}

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base.GetPrefix import *

def do_try(f, *x, **kwds):
  try:
    f(*x, **kwds)
  except Exception as e:
    print('ERROR:', e)
  else:
    raise Exception('Should have failed')
