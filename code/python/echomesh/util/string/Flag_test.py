from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.string import Flag

from echomesh.util.TestCase import TestCase

class FlagTest(TestCase):
    def test_empty(self):
        self.assertEqual(Flag.split_flag(''), (u'', True))

    def test_single_dash(self):
        self.assertEqual(Flag.split_flag('-'), (u'', True))

    def test_single_flag(self):
        self.assertEqual(Flag.split_flag('-x'), (u'x', True))

    def test_double_dash(self):
        self.assertEqual(Flag.split_flag('--hello'), (u'hello', True))

    def test_double_dash_equal(self):
        self.assertEqual(Flag.split_flag('--hello='), (u'hello', True))

    def test_full_flag(self):
        self.assertEqual(Flag.split_flag('--hello=world'), (u'hello', u'world'))

    def test_complex_case(self):
        self.assertEqual(
          Flag.split_flag_args(
              ['hello', '--foo', '--bar=baz', '--bing', 'world']),
          ({u'bing': True, u'foo': True, u'bar': u'baz'}, [u'hello', u'world']))
