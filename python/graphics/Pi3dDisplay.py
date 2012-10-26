from __future__ import absolute_import, division, print_function, unicode_literals

import time

from graphics import Rect
from graphics.pi3d import pi3d

from util import Log
from util import Openable

LOGGING = Log.logger(__name__)

class Pi3dDisplay(Openable.Openable):
  def __init__(self, config):
    Openable.Openable.__init__(self)
    self.config = config
    self.display = pi3d.display()
    self.clients = []
    self.textures = pi3d.textures()
    self.keys = pi3d.key()

    display.create2D(x, y, width, height)
    display.setBackColor(0, 0, 0, 0)  # last is alpha

  def run(self):
    self.display.clear()
    dirty = None
    t = time.time()
    for c in clients:
      dirty = Rect.union(dirty, clients.update(t))
    # Repaint the dirty areas.
    # Flip the screen.
    # Sleep
