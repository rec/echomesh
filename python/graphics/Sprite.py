from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import time

from graphics import Pi3dDisplay

from util.Envelope import Envelope
from util import Log
from util.Openable import Openable

LOGGER = Log.logger(__name__)

DEFAULT_Z = -2.0

class Sprite(Openable):
  def update(self, time):
    """Called on each clock tick.
      time: the time in floating point seconds."""
    LOGGER.info('Closing sprite')
    pass

class ImageSprite(Sprite):
  def __init__(self, display, image=None, loops=1,
               position=(0, 0), rotation=0, size=1, duration=0, z=DEFAULT_Z):
    Sprite.__init__(self)
    self.imagename = image
    self.display = display
    LOGGER.debug('Opening sprite %s', image)

    self.loops = loops
    self.loop_number = 0
    self.position = Envelope(position)
    self.rotation = Envelope(rotation)
    self.size = Envelope(size)
    self.z = Envelope(z)

    self.time = 0
    if duration:
      self.duration = duration
    else:
      envs = [self.position, self.rotation, self.size]
      self.duration = max(x.length() for x in envs)

    display.add_sprite(self)

  def update(self, t):
    if not hasattr(self, 'image'):
      if self.imagename and self.display:
        self.image = self.display.load_texture(self.imagename)
      else:
        self.image = None
        LOGGER.error('No image in image arguments')

    if not self.time:
      self.time = t
    elapsed = t - self.time
    if elapsed > self.duration:
      self.loop_number += 1
      if self.loop_number < self.loops:
        self.time = 0
        elapsed = 0
      else:
        self.close()
        return

    x, y = self.position.interpolate(elapsed)
    z = self.z.interpolate(elapsed)
    size = self.size.interpolate(elapsed)
    width = self.image.ix * size
    height = self.image.iy * size
    rotation = self.rotation.interpolate(elapsed)

    from graphics.pi3d import pi3d
    pi3d.sprite(self.image, x, y, z, width, height, rotation)
