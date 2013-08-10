from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Debounce

from echomesh.util.TestCase import TestCase

class DebounceTest(TestCase):
  def setUp(self):
    self.states = [0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0]
    self._state = None
    self.debouncer = Debounce.Debounce()

  def state(self):
    return self.states.pop(0)

  def update(self, state):
    self._state = state

  def assertState(self, state=None):
    self.debouncer.update()
    self.assertEqual(state, self._state)
    self._state = None

  def test_all(self):
    self.assertTrue(self.debouncer.add_client(self))
    self.assertState()
    self.assertState(0)

    self.assertState()
    self.assertState()
    self.assertState()
    self.assertState()
    self.assertState()
    self.assertState(1)

    self.assertState()
    self.assertState()
    self.assertState()
    self.assertState(0)

    self.assertState()
    self.assertState()
    self.assertState()
