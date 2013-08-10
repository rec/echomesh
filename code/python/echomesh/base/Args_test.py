from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.base import Args
from echomesh.util.TestCase import TestCase

PART = 'x=[{1: 2, 3: 4}]'

class ArgsTest(TestCase):
  def assertTest(self, args, expected):
    try:
      result = Args.split(args)
    except Exception as e:
      result = 'ERROR: %s' % str(e)
    self.assertEqual(result, expected)

  def test_empty(self):
    self.assertTest('', [])

  def test_simple(self):
    self.assertTest('x=2', [['x', 2]])

  def test_assign(self):
    self.assertTest('x=false', [['x', False]])

  def test_assign_string(self):
    self.assertTest('x="a b c"', [['x', 'a b c']])

  def test_failed_equal(self):
    self.assertTest('xyz="',
                    'ERROR: At column 5: unterminated quotation mark.')

  def test_list(self):
    self.assertTest('x=[1, 2, 3]', [['x', [1, 2, 3]]])

  def test_list_2(self):
    self.assertTest('x=[1, 2]', [['x', [1, 2]]])

  def test_dict(self):
    self.assertTest('x={1: 2, 3: 4}', [['x', {1: 2, 3: 4}]])

  def test_list_dict(self):
    self.assertTest('x=[{1: 2, 3: 4}]', [['x', [{1: 2, 3: 4}]]])

  def test_long_assingment(self):
    self.assertTest('light.display.layout=[64, 0]', [['light.display.layout', [64, 0]]])

  def test_reversed_closing(self):
    self.assertTest('x=[{1: 2, 3: 4]}',
                    'ERROR: At column 15: Got closing [ for opening {.')

  def test_part(self):
    self.assertTest(PART, [['x', [{1: 2, 3: 4}]]])

  def test_part_incomplete(self):
    self.assertTest(PART[:-1],
                    'ERROR: At column 15: missing closing brackets in [.')

  def test_part_incomplete_2(self):
    self.assertTest(PART[:-2],
                    'ERROR: At column 14: missing closing brackets in [{.')

  def test_two_assignments(self):
    self.assertTest('x=2 y=3', [['x', 2], ['y', 3]])

  def test_space_in_assignment(self):
    self.assertTest('extra= 32', [['extra', 32]])

  def test_space_in_assignment_2(self):
    self.assertTest('extra =32', [['extra', 32]])

  def test_spaces_in_assignment(self):
    self.assertTest('extra = 32', [['extra', 32]])

  def test_complex(self):
    self.assertTest('ac.de = .defeg.', [['ac.de', '.defeg.']])

  def test_very_complex(self):
    self.assertTest('extra="32 men" ac.de = .defeg. foo = [ bar, baz ]',
                    [['extra', '32 men'], ['ac.de', '.defeg.'],
                    ['foo', ['bar', 'baz']]])
