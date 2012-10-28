from __future__ import absolute_import, division, print_function, unicode_literals

from util.Envelope import Envelope
from util import Log
from util.Openable import Openable

LOGGER = Log.logger(__name__)

DEFAULT_Z = 0.0

class Sprite(Openable):
  def update(self, time):
    """Called on each clock tick.
      time: the time in floating point seconds."""
    pass


class ImageSprite(Sprite):
  def __init__(self, display, image=None, loops=1,
               position=(0, 0), rotation=0, size=1, duration=0, z=DEFAULT_Z):
    Sprite.__init__(self)
    if image and display:
      self.image = display.load_texture(image)
    else:
      self.image = None
      LOGGER.error('No image in image arguments')

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

    from graphics.pi3d import pi3d
    self.sprite = pi3d.sprite
    display.add_sprite(this)

  def update(self, t):
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
    rotation = self.rotation.interpolate(elapsed)

    print('!!!', self.image, x, y, z, size, rotation)
    self.sprite(self.image, x, y, z, size, size, rotation)
    self.count += 1
