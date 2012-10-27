from __future__ import absolute_import, division, print_function, unicode_literals

import time

from graphics import Rect
from graphics.pi3d import pi3d

from util import Log
from util.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

DEFAULT_BACKGROUND = 0, 0, 0, 1.0
ESCAPE_KEY = 27
DEFAULT_FPS = 60.0
READ_KEYS = False
DISABLE = True

scnx=800
scny=600

class Pi3dDisplay(ThreadLoop):
  def __init__(self, echomesh, config):
    ThreadLoop.__init__(self)
    self.config = config
    self.echomesh = echomesh
    self.textures = pi3d.textures()
    self.display = pi3d.display()
    self.sprites = []
    self.keys = pi3d.key()

    dconf = config['display']
    # self.display.create2D(*dconf.get('dimensions', (0, 0, 0, 0, 0)))
    self.display.create2D(100, 100, scnx, scny, 0)

    background = dconf.get('background', DEFAULT_BACKGROUND)
    #self.display.setBackColour(*background)
    self.display.setBackColour(1.0,0.2,0.6,1)

    self.bar = self.textures.loadTexture("graphics/pi3d/textures/bar.png")
    self.bbtitle = self.textures.loadTexture("graphics/pi3d/textures/pi3dbbd.png",True)

  def add_sprite(self, sprite):
    self.sprites.append(sprite)

  def run(self):
    self.display.clear()
    fps = self.config['display'].get('frames_per_second', DEFAULT_FPS)
    if DISABLE:
      pi3d.rectangle(self.bar, 0, scny, scnx, 32)
      pi3d.rectangle(self.bbtitle, 5, scny, 256+5, 32)
      # self.display.swapBuffers()
      # time.sleep(1.0 / fps)
      self.display.swapBuffers()
      return

    if READ_KEYS and self.keys.read() == ESCAPE_KEY:
      echomesh.close()
      self.close()
      LOGGER.info('Closing display')
      return

    t = time.time()
    self.sprites = [s for s in self.sprites if s.is_open]
    for s in self.sprites:
      s.update(t)
    self.display.swapBuffers()

    # time.sleep(1.0 / fps)

  def close(self):
    ThreadLoop.close(self)
    self.keys.close()
    self.textures.deleteAll()
    self.display.destroy()
