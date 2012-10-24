from __future__ import absolute_import, division, print_function, unicode_literals

from graphics import pi3d
from util import Openable

TEXTURES = pi3d.textures()

class Sprite(object):
  def update(self, time):
    """Called on each clock tick.
      time: the time in floating point seconds."""
    pass

class ImageSprite(Sprite):
  def __init__(self, image, rect=None):
    self.texture = TEXTURES.loadTexture(image)
    self.rect =


