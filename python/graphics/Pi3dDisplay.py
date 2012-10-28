from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import time

from graphics import Rect
from graphics.pi3d import pi3d

from util import Log
from util.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

DEFAULT_BACKGROUND = 0, 0, 0, 1.0
ESCAPE_KEY = 27
DEFAULT_FPS = 60.0

DEFAULT_IMAGE_DIRECTORY = os.path.expanduser('~/echomesh/assets/image/')

class Pi3dDisplay(ThreadLoop):
  def __init__(self, echomesh, config):
    ThreadLoop.__init__(self)
    self.config = config
    self.echomesh = echomesh
    self.textures = pi3d.textures()
    self.texture_cache = {}
    self.display = pi3d.display()
    self.sprites = []

    dconf = config['display']
    self.display.create2D(*dconf.get('dimensions', (0, 0, 0, 0, 0)))

    background = dconf.get('background', DEFAULT_BACKGROUND)
    self.display.setBackColour(*background)

  def add_sprite(self, sprite):
    self.sprites.append(sprite)

  def run(self):
    self.display.clear()

    t = time.time()
    self.sprites = [s for s in self.sprites if s.is_open]
    for s in self.sprites:
      s.update(t)
    self.display.swapBuffers()

    fps = self.config['display'].get('frames_per_second', 0)
    if fps and fps > 0:
      time.sleep(1.0 / fps)

  def load_texture(self, imagefile):
    if not imagefile.startswith('/'):
      imagefile = DEFAULT_IMAGE_DIRECTORY + imagefile
    texture = self.texture_cache.get(os.path.expanduser(imagefile), None)
    if not texture:
      texture = self.textures.loadTexture(imagefile)
      self.texture_cache[imagefile] = texture
    return texture

  def close(self):
    ThreadLoop.close(self)
    self.textures.deleteAll()
    self.display.destroy()
