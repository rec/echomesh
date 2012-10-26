from __future__ import absolute_import, division, print_function, unicode_literals

import time

from graphics import Rect
from graphics.pi3d import pi3d

from util import Log
from util.Openable import Openable

LOGGING = Log.logger(__name__)
DEFAULT_BACKGROUND = 0, 0, 0, 1.0

class Pi3dDisplay(Openable):
  def __init__(self, config):
    Openable.__init__(self)
    self.config = config
    self.display = pi3d.display()
    self.clients = []
    self.textures = pi3d.textures()
    self.keys = pi3d.key()

    dconf = config['display']
    self.display.create2D(*dconf.get('dimensions', ()))
    background = dconf.get('background', DEFAULT_BACKGROUND)
    self.display.setBackColour(*background) 
    self.display.clear()
    self.display.swapBuffers()

  def run(self):
    time.sleep(0.5)
    if True:
      return

    self.display.clear()
    dirty = None
    t = time.time()
    for c in clients:
      dirty = Rect.union(dirty, clients.update(t))
    # Repaint the dirty areas.
    # Flip the screen.
    # Sleep

  def close(self):
    Openable.close(self)
    self.display.destroy()
