from __future__ import absolute_import, division, print_function, unicode_literals

import time

from graphics import Rect
from graphics.pi3d import pi3d

from util import Log
from util.Openable import Openable

LOGGING = Log.logger(__name__)
DEFAULT_BACKGROUND = 0, 0, 0, 1.0
ESCAPE_KEY = 27

class Pi3dDisplay(Openable):
  def __init__(self, echomesh, config):
    Openable.__init__(self)
    self.config = config
    self.echomesh = echomesh
    self.display = pi3d.display()
    self.sprites = []
    self.textures = pi3d.textures()
    self.keys = pi3d.key()

    dconf = config['display']
    self.display.create2D(*dconf.get('dimensions', ()))
    background = dconf.get('background', DEFAULT_BACKGROUND)
    self.display.setBackColour(*background)
    self.display.clear()
    self.display.swapBuffers()

  def add_sprite(self, sprite):
    self.sprites.append(sprite)

  def run(self):
    if self.keys.read() == ESCAPE_KEY:
      echomesh.close()
      self.close()
      return

    self.display.clear()
    t = time.time()
    self.sprites = [s for s in self.sprites if s.is_open]
    for s in sprites:
      s.update(t)
    display.swapBuffers()

  def close(self):
    Openable.close(self)
    self.keys.close()
    self.textures.deleteAll()
    self.display.destroy()
