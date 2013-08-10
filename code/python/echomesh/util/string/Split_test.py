from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.string.Split import split_words, pair_split
from echomesh.util.TestCase import TestCase

class SplitTest(TestCase):
  def test_split_simple(self):
    self.assertEqual(split_words('hello, there!'), ['hello,', 'there!'])

  def test_split_empty(self):
    self.assertEqual(split_words(''), [])

  def test_split_one(self):
    self.assertEqual(split_words('one'), ['one'])

  def test_split_two(self):
    self.assertEqual(split_words('one two'), ['one', 'two'])

  def test_split_two_space(self):
    self.assertEqual(split_words(' one two'), ['one', 'two'])

  def test_split_two_spaces(self):
    self.assertEqual(split_words(' one two '), ['one', 'two'])

  def test_pair_split_empty(self):
    self.assertEqual(pair_split([]), [])

  def test_pair_split_one(self):
    self.assertEqual(pair_split(split_words('hello')), [('hello', None)])

  def test_pair_split_two(self):
    self.assertEqual(pair_split(split_words('hello as hell')),
                     [('hello', 'hell')])

  def test_pair_split_three(self):
    self.assertEqual(pair_split(split_words('hello as hell dogs as cats')),
                     [('hello', 'hell'), ('dogs', 'cats')])

  def test_pair_split_two_pair(self):
    self.assertEqual(pair_split(split_words('hello  hell as dogs cats')),
                     [('hello', 'dogs'), ('hell', 'cats')])
