from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Join
from echomesh.util.TestCase import TestCase

class JoinTest(TestCase):
    def test_empty(self):
        self.assertEqual(Join.join_words([]), '')

    def test_one(self):
        self.assertEqual(Join.join_words(['hello']), 'hello')

    def test_two(self):
        self.assertEqual(Join.join_words(['hello', 'goodbye']),
                                         'goodbye and hello')

    def test_three(self):
        self.assertEqual(Join.join_words(['apples', 'oranges', 'pears']),
                                         'apples, oranges, and pears')
