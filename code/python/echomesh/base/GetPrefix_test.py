from __future__ import absolute_import, division, print_function, unicode_literals\

from echomesh.base import GetPrefix
from echomesh.util.TestCase import TestCase

TABLE = {'one': 1, 'two': 2, 'three': 3}
MASTER = {'foo': {'bar': {'baz': 23}}, 'new': {}}

class GetPrefixTest(TestCase):
    def setUp(self):
        self.slave = {}

    def assertException(self, key, message, allow_prefixes=True):
        with self.assertRaises(GetPrefix.PrefixException) as cm:
            GetPrefix.get_prefix(TABLE, key, allow_prefixes=allow_prefixes)
        self.assertEqual(str(cm.exception), message)

    def test_simple(self):
        self.assertEqual(GetPrefix.get_prefix(TABLE, 'one'), ('one', 1))

    def test_prefix(self):
        self.assertEqual(GetPrefix.get_prefix(TABLE, 'o'), ('one', 1))

    def test_no_prefix(self):
        self.assertEqual(
            GetPrefix.get_prefix(TABLE, 'one', allow_prefixes=False),
            ('one', 1))

    def test_bad_prefix(self):
        self.assertException('o', '"o" is not valid', allow_prefixes=False)

    def test_many_prefixes(self):
        self.assertException('t', '"t" matches more than one: three and two')

    def test_assignment(self):
        GetPrefix.set_assignment('foo.bar.baz', 32, MASTER, self.slave)
        self.assertEqual(self.slave, {'foo': {'bar': {'baz': 32}}})

    def test_assignment_prefix(self):
        GetPrefix.set_assignment('f.b.b', 19, MASTER, self.slave)
        self.assertEqual(self.slave, {'foo': {'bar': {'baz': 19}}})

    def test_assignment_unmapped(self):
        GetPrefix.set_assignment('new.foo', 23, MASTER, self.slave,
                                 unmapped_keys=set(['new']))
        self.assertEqual(self.slave, {'new': {'foo': 23}})

    def test_prefix_dict(self):
        pdict = GetPrefix.PrefixDict(TABLE)
        self.assertEqual(pdict['o'], 1)
        with self.assertRaises(GetPrefix.PrefixException) as cm:
            GetPrefix.get_prefix(TABLE, 'x')
        self.assertEqual(str(cm.exception), '"x" is not valid')
