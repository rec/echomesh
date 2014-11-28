from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.string.UniqueName import unique_name
from echomesh.util.TestCase import TestCase

class UniqueNameTest(TestCase):
    def test_empty(self):
        self.assertEqual(unique_name('', []), '')

    def test_missing(self):
        self.assertEqual(unique_name('foo', ['bar', 'baz']), 'foo')

    def test_dupe(self):
        self.assertEqual(unique_name('bar', ['bar', 'baz']), 'bar-2')

    def test_dupe_two(self):
        self.assertEqual(unique_name('bar', ['bar', 'baz', 'bar-1',]), 'bar-2')

    def test_dupe_three(self):
        self.assertEqual(
            unique_name('bar-2', ['bar', 'baz', 'bar-2',]), 'bar-3')
