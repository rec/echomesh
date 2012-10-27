from __future__ import absolute_import, division, print_function, unicode_literals

from graphics.pi3d import pi3d
from util.Envelope import Envelope
from util.Openable import Openable

DEFAULT_Z = -2.0

class Sprite(Openable):
  def update(self, time):
    """Called on each clock tick.
      time: the time in floating point seconds."""
    pass

class ImageSprite(Sprite):
  def __init__(self, image,
               position=(0, 0), rotation=0, size=1, duration=0, z=DEFAULT_Z):
    Sprite.__init__(self)
    self.image = image
    self.position = Envelope(position)
    self.rotation = Envelope(rotation)
    self.size = Envelope(size)
    self.z = Envelope(z)
    self.time = 0
    self.count = 0
    if duration:
      self.duration = duration
    else:
      envs = [self.position, self.rotation, self.size]
      self.duration = max(x.length() for x in envs)

  def update(self, t):
    if not self.time:
      self.time = t
    elapsed = t - self.time
    if elapsed > self.duration:
      self.close()
    else:
      x, y = self.position.interpolate(elapsed)
      z = self.z.interpolate(elapsed)
      size = self.size.interpolate(elapsed)
      rotation = self.rotation.interpolate(elapsed)

      x += self.count
      y += self.count

      print('!!!', self.image, x, y, z, size, rotation)
      pi3d.sprite(self.image, x, y, z, size, size, rotation)
      self.count += 1
