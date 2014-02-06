from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import TestCase

class TestCase(TestCase.TestCase):
  def assertOutput(self, description, before, after):
    description = description.copy()
    description['output'] = {'type': 'test'}
    from echomesh.output.Registry import make_output

    output = make_output(description)
    output.emit_output(before)
    self.assertEqual(output.output[0].data, after)

