from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import random
import time

from config import Config

from graphics import Rect
from graphics.pi3d import pi3d

from util import Log
from util.File import FileExpander
from util.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

DEFAULT_BACKGROUND = 0, 0, 0, 1
DEFAULT_DIMENSIONS = 0, 0, 0, 0, 0

_DCONF = Config.CONFIG.get('display', {})
BACKGROUND = _DCONF.get('background', DEFAULT_BACKGROUND)
DIMENSIONS = _DCONF.get('dimensions', DEFAULT_DIMENSIONS)

DEFAULT_FPS = 60.0

DISPLAY = pi3d.display()
DISPLAY.create2D(*DIMENSIONS)
DISPLAY.setBackColour(*BACKGROUND)

DEFAULT_IMAGE_DIRECTORY = os.path.expanduser('~/echomesh/assets/image/')

TEXTURES = pi3d.textures()

class Pi3dDisplay(ThreadLoop):
  def __init__(self, echomesh, config):
    ThreadLoop.__init__(self)
    self.config = config
    self.echomesh = echomesh
    self.textures = TEXTURES
    self.texture_cache = {}
    self.sprites = []
    self.count = 0
    self.display = DISPLAY
    self.preload()

  def add_sprite(self, sprite):
    self.sprites.insert(0, sprite)

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
    if imagefile == '$random':
      imagefile = random.choice(os.listdir(DEFAULT_IMAGE_DIRECTORY))
    imagefile = os.path.expanduser(imagefile)
    if not imagefile.startswith('/'):
      imagefile = DEFAULT_IMAGE_DIRECTORY + imagefile
    texture = self.texture_cache.get(imagefile, None)
    if not texture:
      LOGGER.info(imagefile)
      try:
        texture = self.textures.loadTexture(imagefile)
      except IOError:
        LOGGER.error("Can't open image file %s", imagefile)
      self.texture_cache[imagefile] = texture
    return texture

  def preload(self):
    if True:
      return
    for imagefile in os.listdir(DEFAULT_IMAGE_DIRECTORY):
      self.load_texture(imagefile)

  def close(self):
    ThreadLoop.close(self)
    self.textures.deleteAll()
    self.display.destroy()
