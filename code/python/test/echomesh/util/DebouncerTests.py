"""
>>> client = TestClient()
>>> debouncer = Debounce.Debounce()
>>> not debouncer.add_client(client)
False

>>> debouncer.update()
>>> debouncer.update()
updated to 0

>>> debouncer.update()
>>> debouncer.update()
>>> debouncer.update()
>>> debouncer.update()
>>> debouncer.update()
>>> debouncer.update()
updated to 1

>>> debouncer.update()
>>> debouncer.update()
>>> debouncer.update()
>>> debouncer.update()
updated to 0

>>> debouncer.update()
>>> debouncer.update()
>>> debouncer.update()

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Debounce

class TestClient(object):
  def __init__(self):
    self.states = [0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0]

  def state(self):
    return self.states.pop(0)

  def update(self, state):
    print('updated to', state)
