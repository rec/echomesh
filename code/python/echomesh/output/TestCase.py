from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import TestCase
from echomesh.output import make_output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class TestCase(TestCase.TestCase):
  def assertOutput(self, description, before, after):
    description = description.copy()
    description['output'] = {'type': 'test'}
    output = make_output(description)
    output.emit_output(before)
    self.assertEqual(output.output[0].data, after)

