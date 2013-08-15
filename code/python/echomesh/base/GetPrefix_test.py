from __future__ import absolute_import, division, print_function, unicode_literals\

from echomesh.base import GetPrefix
from echomesh.util.TestCase import TestCase

TABLE = {'one': 1, 'two': 2, 'three': 3}
MASTER = {'foo': {'bar': {'baz': 23}}, 'new': {}}

class GetPrefixTest(TestCase):
  def setUp(self):
    self.slave = {}

  def test_simple(self):
    self.assertEqual(GetPrefix.get_prefix(TABLE, 'one'), ('one', 1))

  def test_prefix(self):
    self.assertEqual(GetPrefix.get_prefix(TABLE, 'o'), ('one', 1))

  def test_no_prefix(self):
    self.assertEqual(GetPrefix.get_prefix(TABLE, 'one', allow_prefixes=False),
                     ('one', 1))

  def test_bad_prefix(self):
    try:
      GetPrefix.get_prefix(TABLE, 'o', allow_prefixes=False)
    except Exception as e:
      self.assertEqual(str(e), '"o" is not valid')

  def test_no_prefix2(self):
    try:
      GetPrefix.get_prefix(TABLE, 'x', allow_prefixes=False)
    except Exception as e:
      self.assertEqual(str(e), '"x" is not valid')

  def test_many_prefixes(self):
    try:
      GetPrefix.get_prefix(TABLE, 't')
    except Exception as e:
      self.assertEqual(str(e),
                       '"t" matches more than one: three and two')

  def test_assignment(self):
    GetPrefix.set_assignment('foo.bar.baz', 32, MASTER, self.slave)
    self.assertEqual(self.slave, {'foo': {'bar': {'baz': 32}}})

  def test_assignment_prefix(self):
    GetPrefix.set_assignment('f.b.b', 19, MASTER, self.slave,
                             allow_prefixes=True, create=False)
    self.assertEqual(self.slave, {'foo': {'bar': {'baz': 19}}})

  def test_assignment_unmapped(self):
    GetPrefix.set_assignment('new.foo', 23, MASTER, self.slave,
                             unmapped_names=set(['new']))
    self.assertEqual(self.slave, {'new': {'foo': 23}})

