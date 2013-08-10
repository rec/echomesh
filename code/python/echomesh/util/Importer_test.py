from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Importer
from echomesh.util.TestCase import TestCase

class ImporterTest(TestCase):
  def test_sys(self):
    import sys
    self.assertIs(sys, Importer.imp('sys'))

  def test_failure(self):
    try:
      koala = Importer.imp('koala')
    except Exception as e:
      self.assertEqual(
        str(e),
        'You requested a feature that needs the Python library "koala".')

  def test_named_failure(self):
    try:
      koala = Importer.imp('koala', name='marsupials')
    except Exception as e:
      self.assertEqual(
        str(e),
        'You requested a feature that needs the Python library "marsupials".')
