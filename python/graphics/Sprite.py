from __future__ import absolute_import, division, print_function, unicode_literals

from util import Openable

class Sprite(Openable.Openable):
  def __init__(self):
    Openable.Openable.__init__(self):

  def update(self, time):
    """Called on each clock tick.
      time: the time in floating point seconds.

      Returns a Rect representing the area that needs to be repainted."""
    pass
