from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output import make_output
from echomesh.util.TestCase import TestCase

DESCRIPTION = {
  'type': 'map',
  'map': {0: [3, 4], 1: 2},
  'output': {'type': 'test'},
}

FILTER_DESCRIPTION = {
  'type': 'map',
  'map': {0: [3, 4], 1: 2},
  'output': {'type': 'test'},
  'filter': True
}

class MapTest(TestCase):
  def test_map(self):
    output = make_output(DESCRIPTION.copy())
    output.emit_output(['a', 'b', 'c', 'd', 'e'])
    self.assertEqual(output.output[0].data, ['a', 'b', 'b', 'a', 'a'])

  def test_filter(self):
    output = make_output(FILTER_DESCRIPTION.copy())
    output.emit_output(['a', 'b', 'c', 'd', 'e'])
    self.assertEqual(output.output[0].data, [None, None, 'b', 'a', 'a'])

